from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from pytest_lazyfixture import lazy_fixture

from ansible.module_utils.six.moves import builtins  # noqa

from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule


@pytest.fixture
def sw_config():
    return {
        "name": "MySQL DatabaseServer",
        "cmd_regexp": r"/mysqld(\s|$)",
        "pkg_regexp": r"mysql-serve",
        "docker_regexp": r"mysql(?:-.*):",
        'process_type': 'parent',
        'return_children': False
    }


@pytest.fixture
def params_set_one_sw(sw_config, read_json_file):
    params = {
        'software_list': [sw_config],
        'processes': read_json_file('resources/oss-devel/processes.json')
    }
    params.update(read_json_file('resources/oss-devel/ports.json'))
    params['processes'].append(
        {
            "cmdline": "/usr/sbin/mysqld",
            "pid": "83979",
            "ppid": "1",
            "user": "root"
        }
    )
    params['tcp_listen'].append(
        {
            "address": "::",
            "name": "mysqld",
            "pid": 83979,
            "port": 4306,
            "protocol": "tcp",
            "stime": "Tue May 25 15:30:13 2021",
            "user": "mysql"
        }
    )
    expected_result = [{
        "bindings": [{"address": "::",
                      "class": "service",
                      "port": 4306,
                      "protocol": "tcp"}],
        "type": "MySQL DatabaseServer",
        "discovery_time": "2022-05-26T18:00:00+02:00",
        "process": {
            "cmdline": "/usr/sbin/mysqld",
            "listening_ports": [
                4306
            ],
            "pid": "83979",
            "ppid": "1",
            "user": "root"
        },
        "listening_ports": [
            4306
        ]
    }]
    return params, expected_result


@pytest.fixture
def params_set_no_sw(sw_config):
    params = {
        'software_list': [sw_config],
        'processes': [
            {
                "cmdline": "/usr/lib/systemd/systemd --switched-root --system --deserialize 21",
                "pid": "1",
                "ppid": "0",
                "user": "root"
            },
            {
                "cmdline": "/usr/bin/postgres_client must not match regex",
                "pid": "24895",
                "ppid": "1",
                "user": "root"
            }
        ],
        'tcp_listen': [
            {
                "address": "127.0.0.1",
                "name": "other",
                "pid": 24895,
                "port": 2222,
                "protocol": "tcp",
                "stime": "Fri Apr  8 01:14:02 2022",
                "user": "other"
            }
        ],
        'udp_listen': []
    }
    expected_result = []
    return params, expected_result


@pytest.fixture
def params_set_two_sw(sw_config, params_set_one_sw):
    params_set_one_sw[0]['processes'].append(
        {
            "cmdline": "/usr/sbin/mysqld",
            "pid": "93979",
            "ppid": "1",
            "user": "root"
        }
    )
    params_set_one_sw[0]['tcp_listen'].append(
        {
            "address": "::",
            "name": "mysqld",
            "pid": 93979,
            "port": 9306,
            "protocol": "tcp",
            "stime": "Tue May 25 15:30:13 2021",
            "user": "mysql"
        }
    )
    params_set_one_sw[1].append(
        {
            "bindings": [{"address": "::",
                          "class": "service",
                          "port": 9306,
                          "protocol": "tcp"}],
            "type": "MySQL DatabaseServer",
            "discovery_time": "2022-05-26T18:00:00+02:00",
            "process": {
                "cmdline": "/usr/sbin/mysqld",
                "listening_ports": [
                    9306
                ],
                "pid": "93979",
                "ppid": "1",
                "user": "root"
            },
            "listening_ports": [
                9306
            ]
        }
    )
    return params_set_one_sw


@pytest.mark.parametrize(argnames=['params_and_expected_result'],
                         argvalues=[
                             (lazy_fixture('params_set_one_sw'),),
                             (lazy_fixture('params_set_two_sw'),),
                             (lazy_fixture('params_set_no_sw'),)]
                         )
def test_get_software_ok(normalize,
                         params_and_expected_result):
    params, expected_result = params_and_expected_result
    result = ActionModule(*[None] * 6).process_software(**params)
    assert normalize(result) == normalize(expected_result)
