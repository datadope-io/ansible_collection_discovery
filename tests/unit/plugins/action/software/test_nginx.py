from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible.module_utils.six.moves import builtins  # noqa
from pytest_lazyfixture import lazy_fixture

from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule


@pytest.fixture
def sw_config():
    return {
        "name": "Nginx WebServer",
        "cmd_regexp": r"nginx\:?\s*master.*(nginx)?",
        "pkg_regexp": r"nginx",
        "docker_regexp": r"nginx:",
        'process_type': 'parent',
        'return_children': True
    }


@pytest.fixture
def params_set_one_sw(sw_config, read_json_file):
    params = {
        'software_list': [sw_config],
        'processes': read_json_file('resources/oss-devel/processes.json')
    }
    params.update(read_json_file('resources/oss-devel/ports.json'))
    expected_result = [{
        "bindings": [{"address": "0.0.0.0",
                      "class": "service",
                      "port": 443,
                      "protocol": "tcp"},
                     {"address": "0.0.0.0",
                      "class": "service",
                      "port": 80,
                      "protocol": "tcp"}],
        "type": "Nginx WebServer",
        "discovery_time": "2022-05-26T18:00:00+02:00",
        "process": {
            "children": [
                {
                    "children": [],
                    "cmdline": "nginx: worker process",
                    "pid": "23356",
                    "ppid": "23339",
                    "user": "root",
                    "cwd": "/"
                }
            ],
            "cmdline": "nginx: master process nginx -g daemon off;",
            "listening_ports": [
                80,
                443
            ],
            "pid": "23339",
            "ppid": "23319",
            "user": "root",
            "cwd": "/"
        },
        "listening_ports": [
            80,
            443
        ]
    }]
    return params, expected_result


@pytest.fixture
def params_set_no_sw(sw_config):
    params = {
        'software_list': [sw_config],
        "processes": [
            {
                "cmdline": "/usr/lib/systemd/systemd --switched-root --system --deserialize 21",
                "pid": "1",
                "ppid": "0",
                "user": "root",
                "cwd": "/usr/lib/systemd/"
            },
            {
                "cmdline": "/usr/bin/nginx_client must not match regex",
                "pid": "24895",
                "ppid": "1",
                "user": "root",
                "cwd": "/usr/bin/"
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
            "cmdline": "nginx: master process nginx -g daemon off;",
            "cwd": "/",
            "pid": "53339",
            "ppid": "53319",
            "user": "root"
        }
    )
    params_set_one_sw[0]['tcp_listen'].append(
        {
            "address": "::",
            "name": "nginx",
            "pid": 53339,
            "port": 543,
            "protocol": "tcp",
            "stime": "Fri Apr  8 01:15:02 2022",
            "user": "nginx"
        }
    )
    params_set_one_sw[1].append(
        {
            "bindings": [{"address": "::",
                          "class": "service",
                          "port": 543,
                          "protocol": "tcp"}],
            "type": "Nginx WebServer",
            "discovery_time": "2022-05-26T18:00:00+02:00",
            "process": {
                "children": [],
                "cmdline": "nginx: master process nginx -g daemon off;",
                "cwd": "/",
                "listening_ports": [
                    543
                ],
                "pid": "53339",
                "ppid": "53319",
                "user": "root"
            },
            "listening_ports": [
                543
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
