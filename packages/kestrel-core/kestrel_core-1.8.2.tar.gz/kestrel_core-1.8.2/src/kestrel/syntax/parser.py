from datetime import datetime, timedelta
from importlib.util import find_spec
from lark import Lark, Token, Transformer
from lark.visitors import merge_transformers

from firepit.timestamp import to_datetime
from firepit.query import BinnedColumn
from kestrel.utils import unescape_quoted_string, resolve_path
from kestrel.syntax.utils import resolve_uri
from kestrel.deprecating import load_data_file
from kestrel.syntax.ecgpattern import (
    ECGPComparison,
    ECGPJunction,
    ExtCenteredGraphPattern,
    Reference,
)

DEFAULT_VARIABLE = "_"
DEFAULT_SORT_ORDER = "DESC"


def parse_kestrel(
    stmts, default_variable=DEFAULT_VARIABLE, default_sort_order=DEFAULT_SORT_ORDER
):
    # the public parsing interface for Kestrel
    # return abstract syntax tree
    # check kestrel.lark for details
    grammar = load_data_file("kestrel.syntax", "kestrel.lark")
    return Lark(
        grammar,
        parser="lalr",
        transformer=_KestrelT(default_variable, default_sort_order),
    ).parse(stmts)


def parse_ecgpattern(pattern_str) -> ExtCenteredGraphPattern:
    grammar = load_data_file("kestrel.syntax", "ecgpattern.lark")
    paths = find_spec("kestrel.syntax").submodule_search_locations
    return Lark(
        grammar,
        parser="lalr",
        import_paths=paths,
        transformer=merge_transformers(
            _ECGPatternT(), kestrel=_KestrelT(token_prefix="kestrel__")
        ),
    ).parse(pattern_str)


class _ECGPatternT(Transformer):
    def start(self, args):
        return ExtCenteredGraphPattern(args[0])


class _KestrelT(Transformer):
    def __init__(
        self,
        default_variable=DEFAULT_VARIABLE,
        default_sort_order=DEFAULT_SORT_ORDER,
        token_prefix="",
    ):
        # token_prefix is the modification by Lark when using `merge_transformers()`
        self.default_variable = default_variable
        self.default_sort_order = default_sort_order
        self.token_prefix = token_prefix
        super().__init__()

    def start(self, args):
        return args

    def statement(self, args):
        # Kestrel syntax: a statement can only has one command
        stmt = args.pop()
        return stmt

    def assignment(self, args):
        if len(args) > 2:
            variables = self._extract_vars(args)
            stmt = {"command": "merge", "output": variables[0], "inputs": variables[1:]}
        elif len(args) == 2:
            stmt = args[1]
            # the tree is already processed, and the only thing left is the result variable
            # get it using `self._extract_var()`
            stmt["output"] = self._extract_var(args)
            if "command" not in stmt:
                stmt["command"] = "assign"
        else:
            stmt = args[0]
            stmt["output"] = self.default_variable
        return stmt

    def info(self, args):
        return {"command": "info", "input": self._extract_var(args)}

    def disp(self, args):
        packet = {"command": "disp"}
        for arg in args:
            if isinstance(arg, dict):
                packet.update(arg)
        if "attrs" not in packet:
            packet["attrs"] = "*"
        return packet

    def describe(self, args):
        packet = {"command": "describe"}
        packet.update(args[0])
        return packet

    def get(self, args):
        packet = {
            "command": "get",
            "type": self._extract_entity_type(args),
        }

        for item in args:
            if isinstance(item, dict):
                packet.update(item)

        if "timerange" not in packet:
            packet["timerange"] = None

        return packet

    def find(self, args):
        packet = {
            "command": "find",
            "type": self._extract_entity_type(args),
            "relation": self._assert_and_extract_single("RELATION", args).lower(),
            "reversed": self._extract_if_reversed(args),
            "input": self._extract_var(args),
        }

        for item in args:
            if isinstance(item, dict):
                packet.update(item)

        if "timerange" not in packet:
            packet["timerange"] = None

        return packet

    def join(self, args):
        packet = {
            "command": "join",
            "input": _first(args),
            "input_2": _second(args),
        }
        if len(args) == 5:
            packet["attribute_1"] = _fourth(args)
            packet["attribute_2"] = _fifth(args)

        return packet

    def group(self, args):
        packet = {
            "command": "group",
            "attributes": args[2],
            "input": self._extract_var(args),
        }
        aggregations = args[3] if len(args) > 3 else None
        if aggregations:
            packet["aggregations"] = aggregations
        return packet

    def sort(self, args):
        return {
            "command": "sort",
            "attribute": self._extract_attribute(args),
            "input": self._extract_var(args),
            "ascending": self._extract_direction(args),
        }

    def apply(self, args):
        packet = {"command": "apply", "arguments": {}}
        for arg in args:
            if isinstance(arg, dict):
                if "variables" in arg:
                    packet["inputs"] = arg["variables"]
                else:
                    packet.update(arg)
        return packet

    def load(self, args):
        packet = {
            "command": "load",
            "type": self._extract_entity_type(args),
        }
        for arg in args:
            if isinstance(arg, dict):
                packet.update(arg)
        return packet

    def save(self, args):
        packet = {
            "command": "save",
            "input": self._extract_var(args),
        }
        for arg in args:
            if isinstance(arg, dict):
                packet.update(arg)
        return packet

    def new(self, args):
        if len(args) == 1:
            # Try to get entity type from first entity
            data = args[0]
            if isinstance(data, list):
                entity_type = data[0].get("type")
            else:
                entity_type = None
        else:
            entity_type = _first(args)
            data = args[1]
        return {
            "command": "new",
            "type": entity_type,
            "data": data,
        }

    def expression(self, args):
        packet = args[0]
        for arg in args:
            packet.update(arg)
        return packet

    def vtrans(self, args):
        if len(args) == 1:
            return {
                "input": self._extract_var(args),
            }
        else:
            return {
                "input": self._extract_var(args),
                "transformer": args[0],
            }

    def transformer(self, args):
        return args[0]

    def where_clause(self, args):
        pattern = ExtCenteredGraphPattern(args[0])
        return {
            "where": pattern,
        }

    def expression_or(self, args):
        return ECGPJunction("OR", args[0], args[1])

    def expression_and(self, args):
        return ECGPJunction("AND", args[0], args[1])

    def comparison_std(self, args):
        etype, attr = _extract_entity_and_attribute(args[0].value)
        # remove more than one spaces; capitalize op
        op = args[1]
        value = args[2]
        return ECGPComparison(attr, op, value, etype)

    def comparison_null(self, args):
        etype, attr = _extract_entity_and_attribute(args[0].value)
        op = args[1]
        if "NOT" in op:
            op = "!="
        else:
            op = "="
        value = "NULL"
        return ECGPComparison(attr, op, value, etype)

    def value(self, args):
        return args[0]

    def literal_list(self, args):
        if len(args) == 1:
            return args[0]
        else:
            return args

    def literal(self, args):
        return args[0]

    def var_attr(self, args):
        return {"input": _first(args), "attribute": _second(args)}

    def reference_or_simple_string(self, args):
        if len(args) > 1:
            variable = _first(args)
            attribute = _second(args)
            v = Reference(variable, attribute)
        else:
            v = _first(args)
        return v

    def advanced_string(self, args):
        raw = _first(args)
        value = unescape_quoted_string(raw)
        return value

    def number(self, args):
        v = _first(args)
        try:
            return int(v)
        except:
            return float(v)

    def attr_clause(self, args):
        paths = self._assert_and_extract_single("ATTRIBUTES", args)
        return {
            "attrs": paths if paths else "*",
        }

    def sort_clause(self, args):
        return {
            "attribute": self._extract_attribute(args),
            "ascending": self._extract_direction(args),
        }

    def limit_clause(self, args):
        return {
            "limit": int(_first(args)),
        }

    def offset_clause(self, args):
        return {
            "offset": int(_first(args)),
        }

    def timespan_relative(self, args):
        num = int(args[0])
        unit = args[1]
        if unit == "DAY":
            delta = timedelta(days=num)
        elif unit == "HOUR":
            delta = timedelta(hours=num)
        elif unit == "MINUTE":
            delta = timedelta(minutes=num)
        elif unit == "SECOND":
            delta = timedelta(seconds=num)
        stop = datetime.utcnow()
        start = stop - delta
        return {"timerange": (start, stop)}

    def timespan_absolute(self, args):
        start = to_datetime(args[0])
        stop = to_datetime(args[1])
        return {"timerange": (start, stop)}

    def day(self, _args):
        return "DAY"

    def hour(self, _args):
        return "HOUR"

    def minute(self, _args):
        return "MINUTE"

    def second(self, _args):
        return "SECOND"

    def timestamp(self, args):
        return args[0]

    def var_data(self, args):
        if isinstance(args[0], Token):
            # Restore the brackets
            v = "[" + _first(args) + "]"
        else:
            v = args[0]
        return v

    def json_objs(self, args):
        return args

    def json_obj(self, args):
        return dict(args)

    def json_pair(self, args):
        v = _first(args)
        if "ESCAPED_STRING" in args[0].type:
            v = unescape_quoted_string(v)
        return v, args[1]

    def json_value(self, args):
        v = _first(args)
        if args[0].type == self.token_prefix + "ESCAPED_STRING":
            v = unescape_quoted_string(v)
        elif args[0].type == self.token_prefix + "NUMBER":
            v = float(v) if "." in v else int(v)
        return v

    def entity_type(self, args):
        return _first(args)

    def variables(self, args):
        return {"variables": self._extract_vars(args)}

    def stdpath(self, args):
        v = _first(args)
        if args[0].type == self.token_prefix + "PATH_ESCAPED":
            v = unescape_quoted_string(v)
        v = resolve_path(v)
        return {"path": v}

    def datasource(self, args):
        v = _first(args)
        if args[0].type == self.token_prefix + "DATASRC_ESCAPED":
            v = unescape_quoted_string(v)
        v = ",".join(map(resolve_uri, v.split(",")))
        return {"datasource": v}

    def analytics_uri(self, args):
        v = _first(args)
        if args[0].type == self.token_prefix + "ANALYTICS_ESCAPED":
            v = unescape_quoted_string(v)
        return {"analytics_uri": v}

    # automatically put one or more grp_expr into a list
    def grp_spec(self, args):
        return args

    def grp_expr(self, args):
        item = args[0]
        if isinstance(item, Token):
            # an ATTRIBUTE
            return str(item)
        else:
            # bin_func
            return item

    def bin_func(self, args):
        attr = _first(args)
        num = int(_second(args))
        if len(args) >= 3:
            unit = args[2][0]  # Only pass 1st letter (d, h, m, or s)
        else:
            unit = None
        alias = f"{attr}_bin"
        return BinnedColumn(attr, num, unit, alias=alias)

    def agg_list(self, args):
        return [arg for arg in args]

    def agg(self, args):
        func = _first(args).lower()
        attr = _second(args)
        alias = _third(args) if len(args) > 2 else f"{func}_{attr}"
        return {"func": func, "attr": attr, "alias": alias}

    def args(self, args):
        d = {}
        for di in args:
            d.update(di)
        return {"arguments": d}

    def arg_kv_pair(self, args):
        return {_first(args): args[1]}

    def op(self, args):
        return " ".join([arg.upper() for arg in args])

    def op_keyword(self, args):
        return _first(args)

    def null_op(self, args):
        return " ".join([arg.upper() for arg in args])

    def _extract_vars(self, args):
        var_names = []
        for arg in args:
            if hasattr(arg, "type") and arg.type == self.token_prefix + "VARIABLE":
                var_names.append(arg.value)
        if not var_names:
            var_names = [self.default_variable]
        return var_names

    def _extract_var(self, args):
        var_names = self._extract_vars(args)
        assert len(var_names) == 1
        return var_names[0]

    def _assert_and_extract_single(self, arg_type, args):
        items = [
            arg.value
            for arg in args
            if hasattr(arg, "type") and arg.type == self.token_prefix + arg_type
        ]
        assert len(items) <= 1
        return items.pop() if items else None

    def _extract_attribute(self, args):
        # extract a single attribute from the args
        return self._assert_and_extract_single("ATTRIBUTE", args)

    def _extract_entity_type(self, args):
        # extract a single entity type from the args
        return self._assert_and_extract_single("ENTITY_TYPE", args)

    def _extract_direction(self, args):
        # extract sort direction from args
        # default direction if no variable is found
        # return: if descending
        ds = [
            x
            for x in args
            if hasattr(x, "type")
            and (
                x.type == self.token_prefix + "ASC"
                or x.type == self.token_prefix + "DESC"
            )
        ]
        assert len(ds) <= 1
        d = ds.pop().type if ds else self.token_prefix + self.default_sort_order
        return True if d == self.token_prefix + "ASC" else False

    def _extract_if_reversed(self, args):
        rs = [
            x
            for x in args
            if hasattr(x, "type") and x.type == self.token_prefix + "REVERSED"
        ]
        return True if rs else False


def _first(args):
    return args[0].value


def _second(args):
    return args[1].value


def _third(args):
    return args[2].value


def _fourth(args):
    return args[3].value


def _fifth(args):
    return args[4].value


def _last(args):
    return args[-1].value


def _extract_entity_and_attribute(s):
    if ":" in s:
        etype, _, attr = s.partition(":")
    else:
        etype, attr = None, s
    return etype, attr
