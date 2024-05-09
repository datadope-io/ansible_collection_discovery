from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible.module_utils.six.moves import builtins  # noqa

from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule


@pytest.fixture
def sw_config():
    return {
        "name": "MariaDB DatabaseServer",
        "cmd_regexp": r"/MARIADBD(\s|$)",
        "pkg_regexp": r"mariadb-serve",
        "docker_regexp": r"mariadb(?:-.*):",
        'process_type': 'parent',
        'return_children': False,
        'return_packages': True
    }


@pytest.fixture
def params_set_one_sw(sw_config, read_json_file):
    params = {
        'software_list': [sw_config],
        'processes': read_json_file('resources/oss-devel/processes.json'),
        'packages': read_json_file('resources/oss-devel/packages.json')
    }
    params.update(read_json_file('resources/oss-devel/ports.json'))
    expected_result = [{
        "bindings": [{"address": "::",
                      "class": "service",
                      "port": 3306,
                      "protocol": "tcp"}],
        "type": "MariaDB DatabaseServer",
        "discovery_time": "2022-05-26T18:00:00+02:00",
        "process": {
            "cmdline": "/usr/sbin/mariadbd",
            "listening_ports": [
                3306
            ],
            "pid": "73979",
            "ppid": "1",
            "user": "root",
            "cwd": "/usr/sbin/"
        },
        "listening_ports": [
            3306
        ],
        "packages": [
            {
                "arch": "x86_64",
                "epoch": None,
                "name": "MariaDB-server",
                "release": "1.el7.centos",
                "source": "rpm",
                "version": "10.5.10"
            }
        ],
        "version": [
            {
                "number": "10.5.10",
                "type": "package"
            }
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
                "cmdline": "/usr/bin/postgres_client must not match regex",
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
        'udp_listen': [],
        'packages': {
            "MariaDB-client":
                [
                    {
                        "arch": "x86_64",
                        "epoch": None,
                        "name": "MariaDB-client",
                        "release": "1.el7.centos",
                        "source": "rpm",
                        "version": "10.5.10"
                    }
                ],
        }
    }
    expected_result = []
    return params, expected_result


@pytest.fixture
def params_set_two_sw(sw_config, params_set_one_sw):
    params_set_one_sw[0]['processes'].append(
        {
            "cmdline": "/usr/sbin/mariadbd",
            "cwd": "/usr/sbin/",
            "pid": "93979",
            "ppid": "1",
            "user": "root"
        }
    )
    params_set_one_sw[0]['tcp_listen'].append(
        {
            "address": "::",
            "name": "mariadbd",
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
            "type": "MariaDB DatabaseServer",
            "discovery_time": "2022-05-26T18:00:00+02:00",
            "process": {
                "cmdline": "/usr/sbin/mariadbd",
                "cwd": "/usr/sbin/",
                "listening_ports": [
                    9306
                ],
                "pid": "93979",
                "ppid": "1",
                "user": "root"
            },
            "listening_ports": [
                9306
            ],
            "packages": [
                {
                    "arch": "x86_64",
                    "epoch": None,
                    "name": "MariaDB-server",
                    "release": "1.el7.centos",
                    "source": "rpm",
                    "version": "10.5.10"
                }
            ],
            "version": [
                {
                    "number": "10.5.10",
                    "type": "package"
                }
            ]
        }
    )
    return params_set_one_sw


@pytest.mark.parametrize(argnames=['params_and_expected_result'],
                         argvalues=[
                             ('params_set_one_sw',),
                             ('params_set_two_sw',),
                             ('params_set_no_sw',)]
                         )
def test_get_software_ok(normalize,
                         params_and_expected_result,
                         request):
    params_and_expected_result = request.getfixturevalue(params_and_expected_result)
    params, expected_result = params_and_expected_result
    result = ActionModule(*[None] * 6).process_software(**params)
    assert normalize(result) == normalize(expected_result)
