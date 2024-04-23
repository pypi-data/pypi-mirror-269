import json
import os
import pytest

from kestrel.session import Session

from .utils import set_empty_kestrel_config, set_no_prefetch_kestrel_config


@pytest.fixture
def fake_bundle_file():
    cwd = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(cwd, "../../../test-data/test_bundle.json")


@pytest.fixture
def proc_bundle_file():
    cwd = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(cwd, "../../../test-data/doctored-1k.json")


def test_return_table_not_exist(set_empty_kestrel_config, fake_bundle_file):
    with Session() as s:
        stmt = f"""
                conns = get network-traffic
                        from file://{fake_bundle_file}
                        where [network-traffic:dst_port = 22]
                procs = FIND process CREATED conns
                """
        summaries = s.execute(stmt)
    correct_dict = {
        "display": "execution summary",
        "data": {
            "variables updated": [
                {
                    "VARIABLE": "conns",
                    "TYPE": "network-traffic",
                    "#(ENTITIES)": 29,
                    "#(RECORDS)": 29,
                    "ipv4-addr*": 58,
                    "network-traffic*": 0,
                    "user-account*": 29,
                },
                {
                    "VARIABLE": "procs",
                    "TYPE": "process",
                    "#(ENTITIES)": 0,
                    "#(RECORDS)": 0,
                    "ipv4-addr*": 0,
                    "network-traffic*": 0,
                    "user-account*": 0,
                },
            ],
            "footnotes": ["*Number of related records cached."],
        },
    }
    output_dict = summaries[0].to_dict()
    del output_dict["data"]["execution time"]
    assert output_dict == correct_dict


def test_find_srcs(set_empty_kestrel_config, fake_bundle_file):
    with Session() as s:
        stmt = f"""
                conns = get network-traffic
                        from file://{fake_bundle_file}
                        where dst_port = 22
                srcs = FIND ipv4-addr CREATED conns
                """
        s.execute(stmt)
        srcs = s.get_variable("srcs")
        assert len(srcs) == 24


def test_find_srcs_limit(set_empty_kestrel_config, fake_bundle_file):
    with Session() as s:
        stmt = f"""
                conns = get network-traffic
                        from file://{fake_bundle_file}
                        where dst_port = 22
                srcs = FIND ipv4-addr CREATED conns LIMIT 1
                """
        s.execute(stmt)
        srcs = s.get_variable("srcs")
        assert len(srcs) == 1


def test_find_ips_linked_to_process_limit_1(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                procs = get process
                        from file://{proc_bundle_file}
                        where name = 'svchost.exe'
                ips = FIND ipv4-addr LINKED procs LIMIT 1
                """
        s.execute(stmt)
        procs = s.get_variable("procs")
        print(json.dumps(procs, indent=4))
        assert len(procs) == 704
        ips = s.get_variable("ips")
        print(json.dumps(ips, indent=4))
        # FIXME: the LIMIT does not work precisely (OK to leave it for now)
        assert len(ips) == 2


def test_find_ips_linked_to_process_limit_10(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                procs = get process
                        from file://{proc_bundle_file}
                        where name = 'svchost.exe'
                ips = FIND ipv4-addr LINKED procs LIMIT 10
                """
        s.execute(stmt)
        procs = s.get_variable("procs")
        print(json.dumps(procs, indent=4))
        assert len(procs) == 704
        ips = s.get_variable("ips")
        print(json.dumps(ips, indent=4))
        assert len(ips) == 6


def test_find_file_linked_to_process(set_empty_kestrel_config):
    stixshifter_data_url = "https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/data/cybox"
    bundle = f"{stixshifter_data_url}/carbon_black/cb_observed_156.json"
    with Session() as s:
        stmt = f"""
                procs = get process
                        from {bundle}
                        where name = 'svctest.exe'
                files = FIND file LINKED procs
                """
        s.execute(stmt)
        files = s.get_variable("files")
        print(json.dumps(files, indent=4))
        assert len(files) == 3


def test_find_ips_linked_to_process_limit(set_empty_kestrel_config):
    stixshifter_data_url = "https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/data/cybox"
    bundle = f"{stixshifter_data_url}/carbon_black/cb_observed_156.json"
    with Session() as s:
        stmt = f"""
                procs = get process
                        from {bundle}
                        where name = 'svctest.exe'
                ips = FIND ipv4-addr LINKED procs LIMIT 10
                """
        s.execute(stmt)
        ips = s.get_variable("ips")
        print(json.dumps(ips, indent=4))
        assert len(ips) == 6


def test_find_file_loaded_by_process_wmic(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                procs = get process
                        from file://{proc_bundle_file}
                        where command_line LIKE 'wmic%'
                files = FIND file LOADED BY procs
                """
        s.execute(stmt)
        procs = s.get_variable("procs")
        print(json.dumps(procs, indent=4))
        assert len(procs) == 7
        files = s.get_variable("files")
        print(json.dumps(files, indent=4))
        assert len(files) == 1


def test_find_file_linked_to_process_wmic(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                procs = get process
                        from file://{proc_bundle_file}
                        where command_line LIKE 'wmic%'
                files = FIND file LINKED procs
                """
        s.execute(stmt)
        procs = s.get_variable("procs")
        print(json.dumps(procs, indent=4))
        assert len(procs) == 7
        files = s.get_variable("files")
        print(json.dumps(files, indent=4))
        assert len(files) == 2


def test_find_process_created_process_wmic(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                procs = get process
                        from file://{proc_bundle_file}
                        where command_line LIKE 'wmic%'
                parents = FIND process CREATED procs
                """
        s.execute(stmt)
        data = s.get_variable("parents")
        print(json.dumps(data, indent=4))
        assert len(data)


def test_find_refs_resolution_not_reversed_src_ref(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                nt = get network-traffic
                     from file://{proc_bundle_file}
                     where src_port > 0
                p = FIND process CREATED nt
                """
        s.execute(stmt)
        p = s.get_variable("p")
        # assert len(p) == 948  # grep -c opened_connection_refs tests/doctored-1k.json
        assert len(p) >= 948  # FIXME: duplicate process objects


def test_find_refs_resolution_not_reversed_src_ref_limit(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                nt = get network-traffic
                     from file://{proc_bundle_file}
                     where src_port > 0
                p = FIND process CREATED nt LIMIT 10
                """
        s.execute(stmt)
        p = s.get_variable("p")
        # assert len(p) == 948  # grep -c opened_connection_refs tests/doctored-1k.json
        assert len(p) == 10
 

def test_find_refs_resolution_reversed_src_ref(set_empty_kestrel_config, proc_bundle_file):
    with Session(debug_mode=True) as s:
        stmt = f"""
                procs = get process
                        from file://{proc_bundle_file}
                        where name LIKE '%'
                conns = FIND network-traffic CREATED BY procs
                """
        s.execute(stmt)
        conns = s.get_variable("conns")
        assert (
            len(conns) == 853
        )  # FIXME: should be 948, I think (id collisions for network-traffic)

        # DISP with a ref (parent_ref) and ambiguous column (command_line)
        disp_out = s.execute("DISP procs ATTR name, parent_ref.name, command_line")
        data = disp_out[0].to_dict()["data"]
        print(json.dumps(data, indent=4))


def test_find_refs_resolution_reversed_src_ref_limit(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                procs = get process
                        from file://{proc_bundle_file}
                        where name LIKE '%'
                conns = FIND network-traffic CREATED BY procs LIMIT 10
                """
        s.execute(stmt)
        conns = s.get_variable("conns")
        assert (
            len(conns) == 853
        )

        # DISP with a ref (parent_ref) and ambiguous column (command_line)
        disp_out = s.execute("DISP procs ATTR name, parent_ref.name, command_line")
        data = disp_out[0].to_dict()["data"]
        print(json.dumps(data, indent=4))


def test_find_without_where_ext_pattern(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                conns = get network-traffic
                        FROM file://{proc_bundle_file}
                        WHERE network-traffic:src_ref.value = '127.0.0.1'

                procs = FIND process CREATED conns
                """
        s.execute(stmt)

        conns = s.symtable["conns"]
        procs = s.symtable["procs"]

        assert len(conns) == 193
        assert conns.records_count == 203

        assert len(procs) == 471
        assert procs.records_count == 471


# stix_bundle connector does not support extended graph
# disable prefetch to test
def test_find_with_where_ext_pattern(set_no_prefetch_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                conns = get network-traffic
                        FROM file://{proc_bundle_file}
                        WHERE network-traffic:src_ref.value = '127.0.0.1'

                procs = FIND process CREATED conns
                        WHERE ipv4-addr:value = '192.168.1.1'
                """
        s.execute(stmt)

        conns = s.symtable["conns"]
        procs = s.symtable["procs"]

        assert len(conns) == 193
        assert conns.records_count == 203

        assert len(procs) == 203
        assert procs.records_count == 203


def test_find_with_limit(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                conns = get network-traffic
                        FROM file://{proc_bundle_file}
                        WHERE network-traffic:src_ref.value = '127.0.0.1'

                procs = FIND process CREATED conns LIMIT 100
                """
        s.execute(stmt)

        conns = s.symtable["conns"]
        procs = s.symtable["procs"]

        assert len(conns) == 193
        assert conns.records_count == 203

        assert len(procs) == 100
        assert procs.records_count == 100


def test_find_with_where_centered_pattern(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                conns = get network-traffic
                        FROM file://{proc_bundle_file}
                        WHERE network-traffic:src_ref.value = '127.0.0.1'

                procs = FIND process CREATED conns
                        WHERE name = 'vmware.exe'
                """
        s.execute(stmt)

        conns = s.symtable["conns"]
        procs = s.symtable["procs"]

        assert len(conns) == 193
        assert conns.records_count == 203

        assert len(procs) == 1
        assert procs.records_count == 1


def test_find_from_empty_input(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                conns = get network-traffic
                        FROM file://{proc_bundle_file}
                        WHERE network-traffic:src_ref.value = '100.0.0.1'

                procs = FIND process CREATED conns
                        WHERE name = 'vmware.exe'
                """
        s.execute(stmt)

        conns = s.symtable["conns"]
        procs = s.symtable["procs"]

        assert len(conns) == 0
        assert conns.records_count == 0

        assert len(procs) == 0
        assert procs.records_count == 0


def test_find_dir_contained_file(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                files = GET file
                        FROM file://{proc_bundle_file}
                        WHERE name = 'svchost.exe'
                dirs = FIND directory CONTAINED files
                """
        s.execute(stmt)
        files = s.get_variable("files")
        print(json.dumps(files, indent=4))
        dirs = s.get_variable("dirs")
        print(json.dumps(dirs, indent=4))
        assert len(dirs) == 1


def test_find_files_contained_by_dir(set_empty_kestrel_config, proc_bundle_file):
    with Session() as s:
        stmt = f"""
                dirs = GET directory
                       FROM file://{proc_bundle_file}
                       WHERE path = 'C:\\Windows\\System32'
                files = FIND file CONTAINED BY dirs
                """
        s.execute(stmt)
        files = s.get_variable("files")
        print(json.dumps(files, indent=4))
        assert len(files) == 10
