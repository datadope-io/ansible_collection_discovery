from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible.module_utils.six.moves import builtins  # noqa
from pytest_lazyfixture import lazy_fixture

from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule


@pytest.fixture
def sw_config():
    return {
        'name': 'PostgreSQL Database',
        'cmd_regexp': r'postgres:',
        'pkg_regexp': r'postgresql.*-server|postgresql-\d',
        'docker_regexp': 'postgres:',
        'process_type': 'child',
        'return_children': True,
        'return_packages': True
    }


@pytest.fixture
def params_set_one_sw(sw_config, read_json_file):
    params = {
        'software_list': [sw_config],
        'processes': read_json_file('resources/oss-devel/processes.json'),
        'packages': read_json_file('resources/oss-devel/packages.json'),
        'dockers': read_json_file('resources/oss-devel/dockers.json')
    }
    params.update(read_json_file('resources/oss-devel/ports.json'))
    expected_result = [{
        "bindings": [{"address": "0.0.0.0",
                      "class": "service",
                      "port": 5432,
                      "protocol": "tcp"}],
        "type": "PostgreSQL Database",
        "discovery_time": "2022-05-26T18:00:00+02:00",
        "process": {
            "children": [
                {
                    "children": [],
                    "cmdline": "postgres: data: checkpointer process",
                    "cwd": "/",
                    "pid": "28697",
                    "ppid": "28694",
                    "user": "root"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: writer process",
                    "pid": "28698",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: wal writer process",
                    "pid": "28699",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: autovacuum launcher process",
                    "pid": "28700",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: stats collector process",
                    "pid": "28701",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: bgworker: logical replication launcher",
                    "pid": "28702",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(42292) idle",
                    "pid": "30959",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58162) idle",
                    "pid": "48767",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58232) idle",
                    "pid": "48823",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58272) idle",
                    "pid": "48854",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58354) idle",
                    "pid": "48909",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58358) idle",
                    "pid": "48911",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58412) idle",
                    "pid": "48959",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58456) idle",
                    "pid": "48992",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58482) idle",
                    "pid": "49016",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58508) idle",
                    "pid": "49034",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58586) idle",
                    "pid": "49086",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58588) idle",
                    "pid": "49087",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58598) idle",
                    "pid": "49098",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58604) idle",
                    "pid": "49101",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58622) idle",
                    "pid": "49117",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58630) idle",
                    "pid": "49121",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58634) idle",
                    "pid": "49123",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58650) idle",
                    "pid": "49137",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58680) idle",
                    "pid": "49168",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58684) idle",
                    "pid": "49170",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: data: datadope cmdbuild_r2u2 192.168.1.2(58712) idle",
                    "pid": "49189",
                    "ppid": "28694",
                    "user": "root",
                    "cwd": "/"
                }
            ],
            "cmdline": "/usr/pgsql-10/bin/postmaster -D /etc/postgresql/10/data",
            "listening_ports": [
                5432
            ],
            "pid": "28694",
            "ppid": "1",
            "user": "root",
            "cwd": "/usr/pgsql-10/bin/"
        },
        "listening_ports": [
            5432
        ],
        "packages": [
            {
                "arch": "x86_64",
                "epoch": None,
                "name": "postgresql10-server",
                "release": "1PGDG.rhel7",
                "source": "rpm",
                "version": "10.17"
            }
        ],
        "version": [
            {
                "number": "10.17",
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
            "postgresql": [
                {
                    "arch": "x86_64",
                    "epoch": None,
                    "name": "postgresql",
                    "release": "6.el7_9",
                    "source": "rpm",
                    "version": "9.2.24"
                }
            ],
            "postgresql-devel": [
                {
                    "arch": "x86_64",
                    "epoch": None,
                    "name": "postgresql-devel",
                    "release": "6.el7_9",
                    "source": "rpm",
                    "version": "9.2.24"
                }
            ],
            "postgresql-libs": [
                {
                    "arch": "x86_64",
                    "epoch": None,
                    "name": "postgresql-libs",
                    "release": "6.el7_9",
                    "source": "rpm",
                    "version": "9.2.24"
                }
            ]
        }
    }
    expected_result = []
    return params, expected_result


@pytest.fixture
def params_set_two_sw(sw_config, params_set_one_sw):
    params_set_one_sw[0]['processes'].extend([
        {
            "cmdline": "/usr/lib/systemd/systemd --switched-root --system --deserialize 21",
            "pid": "1",
            "ppid": "0",
            "user": "root",
            "cwd": "/usr/lib/systemd/"
        },
        {
            "cmdline": "/usr/pgsql-11/bin/postmaster -D /var/lib/pgsql/11/data/",
            "pid": "34895",
            "ppid": "1",
            "user": "root",
            "cwd": "/usr/pgsql-11/bin/"
        },
        {
            "cmdline": "postgres: logger",
            "pid": "34898",
            "ppid": "34895",
            "user": "root",
            "cwd": "/"
        },
        {
            "cmdline": "postgres: checkpointer",
            "pid": "34900",
            "ppid": "34895",
            "user": "root",
            "cwd": "/"
        },
        {
            "cmdline": "postgres: background writer",
            "pid": "34901",
            "ppid": "34895",
            "user": "root",
            "cwd": "/"
        },
        {
            "cmdline": "postgres: walwriter",
            "pid": "34902",
            "ppid": "34895",
            "user": "root",
            "cwd": "/"
        },
        {
            "cmdline": "postgres: autovacuum launcher",
            "pid": "34903",
            "ppid": "34895",
            "user": "root",
            "cwd": "/"
        },
        {
            "cmdline": "postgres: stats collector",
            "pid": "34904",
            "ppid": "34895",
            "user": "root",
            "cwd": "/"
        },
        {
            "cmdline": "postgres: logical replication launcher",
            "pid": "34905",
            "ppid": "34895",
            "user": "root",
            "cwd": "/"
        }
    ])
    params_set_one_sw[0]['tcp_listen'].extend([
        {
            "address": "127.0.0.1",
            "name": "postmaster",
            "pid": 34895,
            "port": 5432,
            "protocol": "tcp",
            "stime": "Fri Apr  8 01:14:02 2022",
            "user": "postgres"
        }
    ])
    params_set_one_sw[0]['packages'].update({
        "postgresql11": [
            {
                "arch": "x86_64",
                "epoch": None,
                "name": "postgresql11",
                "release": "1PGDG.rhel7",
                "source": "rpm",
                "version": "11.17"
            }
        ],
        "postgresql11-contrib": [
            {
                "arch": "x86_64",
                "epoch": None,
                "name": "postgresql11-contrib",
                "release": "1PGDG.rhel7",
                "source": "rpm",
                "version": "11.17"
            }
        ],
        "postgresql11-libs": [
            {
                "arch": "x86_64",
                "epoch": None,
                "name": "postgresql11-libs",
                "release": "1PGDG.rhel7",
                "source": "rpm",
                "version": "11.17"
            }
        ],
        "postgresql11-server": [
            {
                "arch": "x86_64",
                "epoch": None,
                "name": "postgresql11-server",
                "release": "1PGDG.rhel7",
                "source": "rpm",
                "version": "11.17"
            }
        ]
    })
    params_set_one_sw[1][0]['packages'].append({
        "arch": "x86_64",
        "epoch": None,
        "name": "postgresql11-server",
        "release": "1PGDG.rhel7",
        "source": "rpm",
        "version": "11.17"
    })
    params_set_one_sw[1][0]['version'].append({
        'number': '11.17',
        'type': 'package'
    })
    params_set_one_sw[1].append({
        "bindings": [{"address": "127.0.0.1",
                      "class": "service",
                      "port": 5432,
                      "protocol": "tcp"}],
        "type": "PostgreSQL Database",
        "discovery_time": "2022-05-26T18:00:00+02:00",
        "process": {
            "children": [
                {
                    "children": [],
                    "cmdline": "postgres: logger",
                    "pid": "34898",
                    "ppid": "34895",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: checkpointer",
                    "pid": "34900",
                    "ppid": "34895",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: background writer",
                    "pid": "34901",
                    "ppid": "34895",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: walwriter",
                    "pid": "34902",
                    "ppid": "34895",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: autovacuum launcher",
                    "pid": "34903",
                    "ppid": "34895",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: stats collector",
                    "pid": "34904",
                    "ppid": "34895",
                    "user": "root",
                    "cwd": "/"
                },
                {
                    "children": [],
                    "cmdline": "postgres: logical replication launcher",
                    "pid": "34905",
                    "ppid": "34895",
                    "user": "root",
                    "cwd": "/"
                }
            ],
            "cmdline": "/usr/pgsql-11/bin/postmaster -D /var/lib/pgsql/11/data/",
            "listening_ports": [
                5432
            ],
            "pid": "34895",
            "ppid": "1",
            "user": "root",
            "cwd": "/usr/pgsql-11/bin/"
        },
        "listening_ports": [5432],
        "packages": [
            {
                "arch": "x86_64",
                "epoch": None,
                "name": "postgresql10-server",
                "release": "1PGDG.rhel7",
                "source": "rpm",
                "version": "10.17"},
            {
                "arch": "x86_64",
                "epoch": None,
                "name": "postgresql11-server",
                "release": "1PGDG.rhel7",
                "source": "rpm",
                "version": "11.17"}],
        "version": [
            {
                "number": "10.17",
                "type": "package"
            },
            {
                "number": "11.17",
                "type": "package"
            }
        ]
    })
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
