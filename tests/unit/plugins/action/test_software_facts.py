from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import os.path

import pytest
from ansible.errors import AnsibleError, AnsibleRuntimeError
from ansible.module_utils.six import iteritems

from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import call, patch, MagicMock, ANY
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.__init__ import _TEMPLAR_HAS_TEMPLATE_CACHE
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule


@pytest.fixture
def task_vars():
    return {'inventory_hostname': 'the_host'}


@pytest.fixture
def params_set_child_with_children():
    params = {
        'software_list': [{
            'name': 'SW child with children',
            'cmd_regexp': r'postgres:',
            'pkg_regexp': r'postgresql.*-server|postgresql-\d',
            'docker_regexp': 'postgres:',
            'process_type': 'child',
            'return_children': True,
            'return_packages': True
        }],
        'processes': [
            {
                "cmdline": "/usr/lib/systemd/systemd --switched-root --system --deserialize 21",
                "cwd": "/usr/lib/systemd/",
                "pid": "1",
                "ppid": "0"
            },
            {
                "cmdline": "/usr/pgsql-11/bin/postmaster -D /var/lib/pgsql/11/data/",
                "cwd": "/usr/pgsql-11/bin/",
                "pid": "24895",
                "ppid": "1"
            },
            {
                "cmdline": "postgres: logger",
                "cwd": "/",
                "pid": "24898",
                "ppid": "24895"
            },
            {
                "cmdline": "postgres: checkpointer",
                "cwd": "/",
                "pid": "24900",
                "ppid": "24895"
            },
            {
                "cmdline": "postgres: background writer",
                "cwd": "/",
                "pid": "24901",
                "ppid": "24895"
            },
            {
                "cmdline": "postgres: walwriter",
                "cwd": "/",
                "pid": "24902",
                "ppid": "24895"
            },
            {
                "cmdline": "postgres: autovacuum launcher",
                "cwd": "/",
                "pid": "24903",
                "ppid": "24895"
            },
            {
                "cmdline": "postgres: stats collector",
                "cwd": "/",
                "pid": "24904",
                "ppid": "24895"
            },
            {
                "cmdline": "postgres: logical replication launcher",
                "cwd": "/",
                "pid": "24905",
                "ppid": "24895"
            },
        ],
        'tcp_listen': [
            {
                "address": "127.0.0.1",
                "name": "postmaster",
                "pid": 24895,
                "port": 5432,
                "protocol": "tcp",
                "stime": "Fri Apr  8 01:14:02 2022",
                "user": "postgres"
            }
        ],
        'udp_listen': [],
        'packages': {
            "postgresql":
                [
                    {
                        "arch": "x86_64",
                        "epoch": None,
                        "name": "postgresql",
                        "release": "6.el7_9",
                        "source": "rpm",
                        "version": "9.2.24"
                    }
                ],
            "postgresql-devel":
                [
                    {
                        "arch": "x86_64",
                        "epoch": None,
                        "name": "postgresql-devel",
                        "release": "6.el7_9",
                        "source": "rpm",
                        "version": "9.2.24"
                    }
                ],
            "postgresql-libs":
                [
                    {
                        "arch": "x86_64",
                        "epoch": None,
                        "name": "postgresql-libs",
                        "release": "6.el7_9",
                        "source": "rpm",
                        "version": "9.2.24"
                    }
                ],
            "postgresql10":
                [
                    {
                        "arch": "x86_64",
                        "epoch": None,
                        "name": "postgresql10",
                        "release": "1PGDG.rhel7",
                        "source": "rpm",
                        "version": "10.17"
                    }
                ],
            "postgresql10-contrib":
                [
                    {
                        "arch": "x86_64",
                        "epoch": None,
                        "name": "postgresql10-contrib",
                        "release": "1PGDG.rhel7",
                        "source": "rpm",
                        "version": "10.17"
                    }
                ],
            "postgresql10-libs":
                [
                    {
                        "arch": "x86_64",
                        "epoch": None,
                        "name": "postgresql10-libs",
                        "release": "1PGDG.rhel7",
                        "source": "rpm",
                        "version": "10.17"
                    }
                ],
            "postgresql10-server":
                [
                    {
                        "arch": "x86_64",
                        "epoch": None,
                        "name": "postgresql10-server",
                        "release": "1PGDG.rhel7",
                        "source": "rpm",
                        "version": "10.17"
                    }
                ],
        }
    }
    expected_result = [{
        "bindings": [{"address": "127.0.0.1",
                      "class": "service",
                      "port": 5432,
                      "protocol": "tcp"}],
        "type": "SW child with children",
        "discovery_time": '2022-05-26T17:03:00+02:00',
        "process": {
            "children": [
                {
                    "children": [],
                    "cmdline": "postgres: logger",
                    "cwd": "/",
                    "pid": "24898",
                    "ppid": "24895"
                },
                {
                    "children": [],
                    "cmdline": "postgres: checkpointer",
                    "cwd": "/",
                    "pid": "24900",
                    "ppid": "24895"
                },
                {
                    "children": [],
                    "cmdline": "postgres: background writer",
                    "cwd": "/",
                    "pid": "24901",
                    "ppid": "24895"
                },
                {
                    "children": [],
                    "cmdline": "postgres: walwriter",
                    "cwd": "/",
                    "pid": "24902",
                    "ppid": "24895"
                },
                {
                    "children": [],
                    "cmdline": "postgres: autovacuum launcher",
                    "cwd": "/",
                    "pid": "24903",
                    "ppid": "24895"
                },
                {
                    "children": [],
                    "cmdline": "postgres: stats collector",
                    "cwd": "/",
                    "pid": "24904",
                    "ppid": "24895"
                },
                {
                    "children": [],
                    "cmdline": "postgres: logical replication launcher",
                    "cwd": "/",
                    "pid": "24905",
                    "ppid": "24895"
                }
            ],
            "cmdline": "/usr/pgsql-11/bin/postmaster -D /var/lib/pgsql/11/data/",
            "cwd": "/usr/pgsql-11/bin/",
            "listening_ports": [
                5432
            ],
            "pid": "24895",
            "ppid": "1"
        },
        "listening_ports": [
            5432
        ],
        'packages': [{
            'arch': 'x86_64',
            'epoch': None,
            'name': 'postgresql10-server',
            'release': '1PGDG.rhel7',
            'source': 'rpm',
            'version': '10.17'
        }],
        'version': [{'number': '10.17', 'type': 'package'}]
    }]
    return params, expected_result


@pytest.fixture
def params_set_child_without_children():
    params = {
        'software_list': [{
            'name': 'SW child without children',
            'cmd_regexp': r'postgres:',
            'pkg_regexp': r'postgresql.*-server|postgresql-\d',
            'docker_regexp': 'postgres:',
            'process_type': 'child',
            'return_children': False
        }],
        "processes": [
            {
                "cmdline": "/usr/lib/systemd/systemd --switched-root --system --deserialize 21",
                "cwd": "/usr/lib/systemd/",
                "pid": "1",
                "ppid": "0"
            },
            {
                "cmdline": "/usr/pgsql-11/bin/postmaster -D /var/lib/pgsql/11/data/",
                "pid": "24895",
                "ppid": "1",
                "cwd": "/usr/pgsql-11/bin/"
            },
            {
                "cmdline": "postgres: logger",
                "pid": "24898",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: checkpointer",
                "pid": "24900",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: background writer",
                "pid": "24901",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: walwriter",
                "pid": "24902",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: autovacuum launcher",
                "pid": "24903",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: stats collector",
                "pid": "24904",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: logical replication launcher",
                "pid": "24905",
                "ppid": "24895",
                "cwd": "/"
            }
        ],
        'tcp_listen': [
            {
                "address": "127.0.0.1",
                "name": "postmaster",
                "pid": 24895,
                "port": 5432,
                "protocol": "tcp",
                "stime": "Fri Apr  8 01:14:02 2022",
                "user": "postgres"
            }
        ],
        'udp_listen': []
    }
    expected_result = [{
        "bindings": [{"address": "127.0.0.1",
                      "class": "service",
                      "port": 5432,
                      "protocol": "tcp"}],
        "type": "SW child without children",
        "discovery_time": '2022-05-26T17:03:00+02:00',
        "process": {
            "cmdline": "/usr/pgsql-11/bin/postmaster -D /var/lib/pgsql/11/data/",
            "cwd": "/usr/pgsql-11/bin/",
            "listening_ports": [
                5432
            ],
            "pid": "24895",
            "ppid": "1"
        },
        "listening_ports": [
            5432
        ]
    }]
    return params, expected_result


@pytest.fixture
def params_set_parent_with_children():
    params = {
        'software_list': [{
            'name': 'SW parent with children',
            'cmd_regexp': r'postmaster',
            'pkg_regexp': r'postgresql.*-server|postgresql-\d',
            'docker_regexp': 'postgres:',
            'process_type': 'parent',
            'return_children': True
        }],
        "processes": [
            {
                "cmdline": "/usr/lib/systemd/systemd --switched-root --system --deserialize 21",
                "pid": "1",
                "ppid": "0",
                "cwd": "/usr/lib/systemd/"
            },
            {
                "cmdline": "/usr/pgsql-11/bin/postmaster -D /var/lib/pgsql/11/data/",
                "pid": "24895",
                "ppid": "1",
                "cwd": "/usr/pgsql-11/bin/"
            },
            {
                "cmdline": "postgres: logger",
                "pid": "24898",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: checkpointer",
                "pid": "24900",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: background writer",
                "pid": "24901",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: walwriter",
                "pid": "24902",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: autovacuum launcher",
                "pid": "24903",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: stats collector",
                "pid": "24904",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: logical replication launcher",
                "pid": "24905",
                "ppid": "24895",
                "cwd": "/"
            }
        ],
        'tcp_listen': [
            {
                "address": "127.0.0.1",
                "name": "postmaster",
                "pid": 24895,
                "port": 5432,
                "protocol": "tcp",
                "stime": "Fri Apr  8 01:14:02 2022",
                "user": "postgres"
            }
        ],
        'udp_listen': [],
        'packages': {
            "postgresql10-server": [
                {
                    "arch": "x86_64",
                    "epoch": None,
                    "name": "postgresql10-server",
                    "release": "1PGDG.rhel7",
                    "source": "rpm",
                    "version": "10.17"
                }
            ],
            'package2': [
                {
                    'name': 'package2',
                    'version': '1'
                },
                {
                    'name': 'package2',
                    'version': '2'
                }
            ]
        },
        'dockers': {
            'containers': [
                {
                    'name': 'container1',
                    'image': 'docker_image1:1'
                },
                {
                    'name': 'container2',
                    'image': 'docker_image2:1'
                }
            ]
        }
    }
    expected_result = [{
        "bindings": [{"address": "127.0.0.1",
                      "class": "service",
                      "port": 5432,
                      "protocol": "tcp"}],
        "type": "SW parent with children",
        "discovery_time": '2022-05-26T17:03:00+02:00',
        "process": {
            "children": [
                {
                    "children": [],
                    "cmdline": "postgres: logger",
                    "cwd": "/",
                    "pid": "24898",
                    "ppid": "24895"
                },
                {
                    "children": [],
                    "cmdline": "postgres: checkpointer",
                    "cwd": "/",
                    "pid": "24900",
                    "ppid": "24895"
                },
                {
                    "children": [],
                    "cmdline": "postgres: background writer",
                    "cwd": "/",
                    "pid": "24901",
                    "ppid": "24895"
                },
                {
                    "children": [],
                    "cmdline": "postgres: walwriter",
                    "cwd": "/",
                    "pid": "24902",
                    "ppid": "24895"
                },
                {
                    "children": [],
                    "cmdline": "postgres: autovacuum launcher",
                    "cwd": "/",
                    "pid": "24903",
                    "ppid": "24895"
                },
                {
                    "children": [],
                    "cmdline": "postgres: stats collector",
                    "cwd": "/",
                    "pid": "24904",
                    "ppid": "24895"
                },
                {
                    "children": [],
                    "cmdline": "postgres: logical replication launcher",
                    "cwd": "/",
                    "pid": "24905",
                    "ppid": "24895"
                }
            ],
            "cmdline": "/usr/pgsql-11/bin/postmaster -D /var/lib/pgsql/11/data/",
            "cwd": "/usr/pgsql-11/bin/",
            "listening_ports": [
                5432
            ],
            "pid": "24895",
            "ppid": "1"
        },
        "listening_ports": [
            5432
        ],
        'version': [
            {
                "type": "package",
                "number": "10.17"
            }
        ]
    }]
    return params, expected_result


@pytest.fixture
def params_set_parent_without_children():
    params = {
        'software_list': [{
            'name': 'SW parent without children',
            'cmd_regexp': r'postmaster',
            'pkg_regexp': r'postgresql.*-server|postgresql-\d',
            'docker_regexp': 'postgres:',
            'process_type': 'parent',
            'return_children': False
        }],
        "processes": [
            {
                "cmdline": "/usr/lib/systemd/systemd --switched-root --system --deserialize 21",
                "pid": "1",
                "ppid": "0",
                "cwd": "/usr/lib/systemd/"
            },
            {
                "cmdline": "/usr/pgsql-11/bin/postmaster -D /var/lib/pgsql/11/data/",
                "pid": "24895",
                "ppid": "1",
                "cwd": "/usr/pgsql-11/bin/"
            },
            {
                "cmdline": "postgres: logger",
                "pid": "24898",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: checkpointer",
                "pid": "24900",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: background writer",
                "pid": "24901",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: walwriter",
                "pid": "24902",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: autovacuum launcher",
                "pid": "24903",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: stats collector",
                "pid": "24904",
                "ppid": "24895",
                "cwd": "/"
            },
            {
                "cmdline": "postgres: logical replication launcher",
                "pid": "24905",
                "ppid": "24895",
                "cwd": "/"
            }
        ],
        'tcp_listen': [
            {
                "address": "127.0.0.1",
                "name": "postmaster",
                "pid": 24895,
                "port": 5432,
                "protocol": "tcp",
                "stime": "Fri Apr  8 01:14:02 2022",
                "user": "postgres"
            }
        ],
        'udp_listen': [],
        'packages': {
            'package1': [
                {
                    'name': 'package1',
                    'version': '1'
                },
                {
                    'name': 'package1',
                    'version': '2'
                }
            ],
            'package2': [
                {
                    'name': 'package2',
                    'version': '1'
                },
                {
                    'name': 'package2',
                    'version': '2'
                }
            ]
        },
        'dockers': {
            'containers': [
                {
                    'name': 'container1',
                    'image': 'docker_image1:1'
                },
                {
                    'name': 'container2',
                    'image': 'docker_image2:1'
                }
            ]
        }
    }
    expected_result = [{
        "bindings": [{"address": "127.0.0.1",
                      "class": "service",
                      "port": 5432,
                      "protocol": "tcp"}],
        "type": "SW parent without children",
        "discovery_time": '2022-05-26T17:03:00+02:00',
        "process": {
            "cmdline": "/usr/pgsql-11/bin/postmaster -D /var/lib/pgsql/11/data/",
            "cwd": "/usr/pgsql-11/bin/",
            "listening_ports": [
                5432
            ],
            "pid": "24895",
            "ppid": "1"
        },
        "listening_ports": [
            5432
        ],
        'version': []
    }]
    return params, expected_result


@pytest.fixture
def params_set_dockers_with_children():
    params = {
        'software_list': [{
            'name': 'SW dockers with childrem',
            'cmd_regexp': r"\.apache\.tomcat\.startup|\.apache\.catalina\.startup",
            'pkg_regexp': r"tomcat",
            'docker_regexp': r"tomcat(?:-.*):",
            'process_type': 'child',
            'return_children': True
        }],
        "processes": [
            {
                "cmdline": "/bin/sh -c /usr/local/bin/docker-entrypoint.sh catalina.sh run",
                "pid": "30709",
                "ppid": "30689",
                "cwd": "/bin/"
            },
            {
                "cmdline":
                    "/usr/local/openjdk-17/bin/java "
                    "-Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties "
                    "-Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager "
                    "-Xmx7876m -Xms3846m "
                    "-Djdk.tls.ephemeralDHKeySize=2048 "
                    "-Djava.protocol.handler.pkgs=org.apache.catalina.webresources "
                    "-Dorg.apache.catalina.security.SecurityListener.UMASK=0027 "
                    "-Xlog:gc=debug:file=logs/gc.log:time,uptime,level,tags:filecount=10,filesize=100m "
                    "-javaagent:/usr/local/tomcat/lib/elastic-apm-agent-1.28.1.jar "
                    "-Delastic.apm.service_name=cmdb "
                    "-Delastic.apm.server_url=http://192.168.8.53:8200 "
                    "-Delastic.apm.environment=dev "
                    "-Delastic.apm.enabled=true "
                    "-Delastic.apm.profiling_inferred_spans_enabled=true "
                    "-Delastic.apm.profiling_inferred_spans_min_duration=250ms "
                    "-Delastic.apm.profiling_inferred_spans_included_classes=org.cmdbuild.* "
                    "-Dignore.endorsed.dirs= -classpath "
                    "/usr/local/tomcat/bin/bootstrap.jar:/usr/local/tomcat/bin/tomcat-juli.jar "
                    "-Dcatalina.base=/usr/local/tomcat "
                    "-Dcatalina.home=/usr/local/tomcat "
                    "-Djava.io.tmpdir=/usr/local/tomcat/temp "
                    "org.apache.catalina.startup.Bootstrap "
                    "start",
                "pid": "30748",
                "ppid": "30709",
                "cwd": "/usr/local/openjdk-17/bin/"
            },
            {
                "cmdline": "/usr/bin/docker-proxy -proto tcp -host-ip :: "
                           "-host-port 9443 -container-ip :: -container-port 9443",
                "pid": "50674",
                "ppid": "80677",
                "cwd": "/usr/bin/"
            },
            {
                "cmdline": "/usr/bin/docker-proxy -host-ip 0.0.0.0 -host-port 8543 "
                           "-container-ip 192.168.1.3 -container-port 8543",
                "pid": "60674",
                "ppid": "70677",
                "cwd": "/usr/bin/"
            },
            {
                "cmdline": "/usr/bin/docker-proxy -host-ip 0.0.0.0 -host-port 8643 "
                           "-container-ip 192.168.1.4 -container-port 8543",
                "pid": "70674",
                "ppid": "90677",
                "cwd": "/usr/bin/"
            },
            {
                "cmdline": "/usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 8743 "
                           "-container-ip 192.168.1.5 -container-port 8543",
                "pid": "80674",
                "ppid": "90679",
                "cwd": "/usr/bin/"
            },
            {
                "cmdline": "/usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 8443 "
                           "-container-ip 192.168.1.2 -container-port 8443",
                "pid": "30674",
                "ppid": "60677",
                "cwd": "/usr/bin/"
            }
        ],
        'tcp_listen': [
            {
                "address": "0.0.0.0",
                "name": "docker-proxy",
                "pid": 30674,
                "port": 8443,
                "protocol": "tcp",
                "stime": "Mon Apr 18 15:33:41 2022",
                "user": "root"
            },
            {
                "address": "0.0.0.0",
                "name": "tcp-test",
                "pid": 60674,
                "port": 8445,
                "protocol": "tcp",
                "stime": "Mon Apr 18 15:33:41 2022",
                "user": "root"
            }
        ],
        'udp_listen': [
            {
                "address": "0.0.0.0",
                "name": "udp-test",
                "pid": 60675,
                "port": 137,
                "protocol": "udp",
                "stime": "Mon Apr 18 15:33:41 2022",
                "user": "root"
            },
            {
                "address": "0.0.0.0",
                "name": "udp-test",
                "pid": 70674,
                "port": 138,
                "protocol": "udp",
                "stime": "Mon Apr 18 15:33:41 2022",
                "user": "root"
            }
        ],
        'dockers': {
            # Only necessary values to software_facts from container info
            'containers': [
                {
                    'Id': '0123456789',
                    'State': {
                        'Pid': 30709
                    },
                    'Config': {
                        'Image': 'nexusregistry.opensolutions.cloud/iometrics-cmdbuild:0.5.3'
                    },
                    'HostConfig': {
                        'NetworkMode': 'host',
                        'PortBindings': {}
                    },
                    'Name': '/iometrics-cmdbuild',
                    'NetworkSettings': {
                        'Gateway': '192.168.1.1',
                        'Networks': {
                            'bridge': {
                                'IPAddress': '192.168.1.2',
                            }
                        }
                    }
                },
                {
                    'State': {
                        'Pid': 60674
                    },
                    'Config': {
                        'Image': 'nexusregistry.opensolutions.cloud/iometrics-cmdb-gateway:0.18.0'
                    },
                    'HostConfig': {
                        'NetworkMode': 'host',
                        'PortBindings': {}
                    },
                    'Name': '/iometrics-cmdb-gateway',
                    'NetworkSettings': {
                        'IPAddress': '192.168.1.3',
                        'Networks': {
                            'host': {
                                'IPAddress': '192.168.1.3',
                            }
                        }
                    }
                },
                {
                    'State': {
                        'Pid': 34206
                    },
                    'Config': {
                        'Image': 'nexusregistry.opensolutions.cloud/iometrics-cmdb-redis-cleaner:0.0.1'
                    },
                    'HostConfig': {
                        'NetworkMode': 'host',
                        'PortBindings': {}
                    },
                    'Name': '/iometrics-cmdb-redis-cleaner',
                    'NetworkSettings': {
                        'IPAddress': '192.168.1.4',
                        'Networks': {
                            'host': {
                                'IPAddress': '',
                            }
                        }
                    }
                },
                {
                    'State': {
                        'Pid': 20064
                    },
                    'Config': {
                        'Image': 'redis:6.0.1'
                    },
                    'HostConfig': {
                        'NetworkMode': 'host',
                        'PortBindings': {}
                    },
                    'Name': '/redis',
                    'NetworkSettings': {
                        'IPAddress': '192.168.1.5',
                        'Networks': {
                            'host': {
                                'IPAddress': ''
                            }
                        }
                    }
                }
            ]
        }
    }
    expected_result = [
        {
            "bindings": [{"address": "0.0.0.0",
                          "class": "service",
                          "port": 8443,
                          "protocol": "tcp"}],
            "type": "SW dockers with childrem",
            "discovery_time": '2022-05-26T17:03:00+02:00',
            "process": {
                "children": [
                    {
                        "children": [],
                        "cmdline": "/usr/local/openjdk-17/bin/java "
                                   "-Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties "
                                   "-Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager "
                                   "-Xmx7876m -Xms3846m "
                                   "-Djdk.tls.ephemeralDHKeySize=2048 "
                                   "-Djava.protocol.handler.pkgs=org.apache.catalina.webresources "
                                   "-Dorg.apache.catalina.security.SecurityListener.UMASK=0027 "
                                   "-Xlog:gc=debug:file=logs/gc.log:time,uptime,level,tags:filecount=10,filesize=100m "
                                   "-javaagent:/usr/local/tomcat/lib/elastic-apm-agent-1.28.1.jar "
                                   "-Delastic.apm.service_name=cmdb "
                                   "-Delastic.apm.server_url=http://192.168.8.53:8200 "
                                   "-Delastic.apm.environment=dev "
                                   "-Delastic.apm.enabled=true "
                                   "-Delastic.apm.profiling_inferred_spans_enabled=true "
                                   "-Delastic.apm.profiling_inferred_spans_min_duration=250ms "
                                   "-Delastic.apm.profiling_inferred_spans_included_classes=org.cmdbuild.* "
                                   "-Dignore.endorsed.dirs= -classpath "
                                   "/usr/local/tomcat/bin/bootstrap.jar:/usr/local/tomcat/bin/tomcat-juli.jar "
                                   "-Dcatalina.base=/usr/local/tomcat "
                                   "-Dcatalina.home=/usr/local/tomcat "
                                   "-Djava.io.tmpdir=/usr/local/tomcat/temp "
                                   "org.apache.catalina.startup.Bootstrap "
                                   "start",
                        "cwd": "/usr/local/openjdk-17/bin/",
                        "pid": "30748",
                        "ppid": "30709"}],
                "cmdline": "/bin/sh -c /usr/local/bin/docker-entrypoint.sh catalina.sh run",
                "cwd": "/bin/",
                "listening_ports": [
                    8443
                ],
                "pid": "30709",
                "ppid": "30689"
            },
            "listening_ports": [
                8443
            ],
            "docker": {
                'id': '0123456789',
                'exposed_ports': {},
                "name": "/iometrics-cmdbuild",
                "network_mode": "host",
                "image": "nexusregistry.opensolutions.cloud/iometrics-cmdbuild:0.5.3",
                'port_bindings': {}
            },
            "version": [
                {
                    "type": "docker",
                    "number": "0.5.3"
                }
            ]
        }]
    return params, expected_result


@pytest.fixture
def params_set_dockers_without_children():
    params = {
        'software_list': [{
            'name': 'SW dockers with childrem',
            'cmd_regexp': r"\.apache\.tomcat\.startup|\.apache\.catalina\.startup",
            'pkg_regexp': r"tomcat",
            'docker_regexp': r"tomcat(?:-.*):",
            'process_type': 'child',
            'return_children': False
        }],
        "processes": [
            {
                "cmdline": "/bin/sh -c /usr/local/bin/docker-entrypoint.sh catalina.sh run",
                "pid": "30709",
                "ppid": "30689",
                "cwd": "/bin/"
            },
            {
                "cmdline": "/usr/local/openjdk-17/bin/java "
                           "-Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties "
                           "-Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Xmx7876m -Xms3846m "
                           "-Djdk.tls.ephemeralDHKeySize=2048 "
                           "-Djava.protocol.handler.pkgs=org.apache.catalina.webresources "
                           "-Dorg.apache.catalina.security.SecurityListener.UMASK=0027 "
                           "-Xlog:gc=debug:file=logs/gc.log:time,uptime,level,tags:filecount=10,filesize=100m "
                           "-javaagent:/usr/local/tomcat/lib/elastic-apm-agent-1.28.1.jar "
                           "-Delastic.apm.service_name=cmdb -Delastic.apm.server_url=http://192.168.8.53:8200 "
                           "-Delastic.apm.environment=dev -Delastic.apm.enabled=true "
                           "-Delastic.apm.profiling_inferred_spans_enabled=true "
                           "-Delastic.apm.profiling_inferred_spans_min_duration=250ms "
                           "-Delastic.apm.profiling_inferred_spans_included_classes=org.cmdbuild.* "
                           "-Dignore.endorsed.dirs= "
                           "-classpath /usr/local/tomcat/bin/bootstrap.jar:/usr/local/tomcat/bin/tomcat-juli.jar "
                           "-Dcatalina.base=/usr/local/tomcat -Dcatalina.home=/usr/local/tomcat "
                           "-Djava.io.tmpdir=/usr/local/tomcat/temp org.apache.catalina.startup.Bootstrap start",
                "pid": "30748",
                "ppid": "30709",
                "cwd": "/usr/local/openjdk-17/bin/"
            },
            {
                "cmdline": "/usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 8443 "
                           "-container-ip 192.168.1.2 -container-port 8443",
                "pid": "30674",
                "ppid": "60677",
                "cwd": "/usr/bin/"
            }
        ],
        'tcp_listen': [
            {
                "address": "0.0.0.0",
                "name": "docker-proxy",
                "pid": 30674,
                "port": 8443,
                "protocol": "tcp",
                "stime": "Mon Apr 18 15:33:41 2022",
                "user": "root"
            }
        ],
        'udp_listen': [],
        'dockers': {
            # Only necessary values to software_facts from container info
            'containers': [
                {
                    'Id': '0123456789',
                    'State': {
                        'Pid': 30709
                    },
                    'Config': {
                        'Image': 'nexusregistry.opensolutions.cloud/iometrics-cmdbuild'
                    },
                    'HostConfig': {
                        'NetworkMode': 'host',
                        'PortBindings': {}
                    },
                    'Name': '/iometrics-cmdbuild',
                    'NetworkSettings': {
                        'Gateway': '192.168.1.1',
                        'Networks': {
                            'bridge': {
                                'IPAddress': '192.168.1.2',
                            }
                        }
                    }
                }
            ]
        }
    }
    expected_result = [
        {
            "bindings": [{"address": "0.0.0.0",
                          "class": "service",
                          "port": 8443,
                          "protocol": "tcp"}],
            'type': 'SW dockers with childrem',
            "discovery_time": '2022-05-26T17:03:00+02:00',
            'process': {
                'cmdline': '/bin/sh -c /usr/local/bin/docker-entrypoint.sh catalina.sh run',
                'cwd': '/bin/',
                'listening_ports': [8443],
                'pid': '30709',
                'ppid': '30689'
            },
            'listening_ports': [
                8443
            ],
            'docker': {
                'exposed_ports': {},
                'id': '0123456789',
                'image': 'nexusregistry.opensolutions.cloud/iometrics-cmdbuild',
                'name': '/iometrics-cmdbuild',
                'network_mode': 'host',
                'port_bindings': {},
            }
        }]
    return params, expected_result


def test_init(action_module):
    instance = action_module(ActionModule)
    expected_args = ['udp_listen', 'software_list', 'processes', 'tcp_listen', 'packages', 'dockers',
                     'pre_tasks', 'post_tasks', 'include_software', 'exclude_software']
    expected_arg_info_list = dict(type='list', elements='dict', required=True)
    expected_arg_info_dict = dict(type='dict', required=False)
    expected_arg_info_list_nonreq = dict(type='list', elements='dict', required=False)
    expected_arg_info = {
        'udp_listen': expected_arg_info_list,
        'software_list': expected_arg_info_list,
        'processes': expected_arg_info_list,
        'tcp_listen': expected_arg_info_list,
        'packages': expected_arg_info_dict,
        'dockers': expected_arg_info_dict,
        'pre_tasks': expected_arg_info_list_nonreq,
        'post_tasks': expected_arg_info_list_nonreq,
        'include_software': dict(type='list', elements='str', required=False),
        'exclude_software': dict(type='list', elements='str', required=False)
    }
    argument_spec = instance.argument_spec
    assert set(argument_spec.keys()) == set(expected_args)
    for arg in argument_spec:
        assert argument_spec[arg] == expected_arg_info[arg]


@pytest.mark.parametrize(
    argnames=('params', 'expected_result'),
    argvalues=[
        (
                'params_set_child_with_children', True
        ),
        (
                {
                    'software_list': [],
                    'processes': [],
                    'tcp_listen': [],
                    'udp_listen': [],
                    'packages': {},
                    'dockers': {}
                }, True
        ),
        (
                {
                    'software_list': {},
                    'processes': [],
                    'tcp_listen': [],
                    'udp_listen': [],
                    'packages': {},
                    'dockers': {}
                }, False
        ),
        (
                {
                    'software_list': ["texto"],
                    'processes': [],
                    'tcp_listen': [],
                    'udp_listen': [],
                    'packages': {},
                    'dockers': {}
                }, False
        ),
        (
                {
                    'software_list': [],
                    'processes': [],
                    'tcp_listen': [],
                    'udp_listen': [],
                    'packages': [],
                    'dockers': {}
                }, False
        ),
        (
                {
                    'software_list': [],
                    'processes': [],
                    'tcp_listen': [],
                    'udp_listen': [],
                    'packages': {},
                    'dockers': []
                }, False
        ),
        (
                {
                    'software_list': [],
                    'tcp_listen': [],
                    'udp_listen': [],
                    'packages': {},
                    'dockers': {}
                }, False
        )
    ])
def test_validate_parameters(action_module, params, expected_result, request):
    if isinstance(params, str):
        params = request.getfixturevalue(params)
    instance = action_module(ActionModule)
    assert instance.validate_parameters(params[0] if isinstance(params, tuple) else params) is expected_result


def test_run_skipped(action_module, task_vars):
    class _ParentClass:

        def __init__(self, *args, **kwargs):
            return  # noqa

        def run(self, *args, **kwargs):  # noqa
            return {'skipped': True}

    instance = action_module(ActionModule, check_mode=True)

    with patch('ansible_collections.datadope.discovery.plugins.action.software_facts.super') as mock_super:
        mock_super.return_value = _ParentClass()
        result = instance.run(None, task_vars)
    assert result['skipped'] is True


def test_run_check_mode(action_module, task_vars):
    instance = action_module(ActionModule, check_mode=True)
    result = instance.run(None, task_vars)
    assert result == {}


def test_run_wrong_parameters(action_module, task_vars, params_set_child_with_children):
    class _ParentClass:

        def __init__(self, *args, **kwargs):
            return  # noqa

        def run(self, *args, **kwargs):  # noqa
            return {}

    instance = action_module(ActionModule)
    instance._task.args = params_set_child_with_children[0]

    with patch.object(instance, 'validate_parameters', return_value=False):
        with patch('ansible_collections.datadope.discovery.plugins.action.software_facts.super') as mock_super:
            mock_super.return_value = _ParentClass()
            with pytest.raises(AnsibleError) as exc_info:
                instance.run(None, task_vars)
    assert exc_info.value.args[0] == 'Parameter validation failed'


def test_run(action_module, task_vars, params_set_child_with_children, normalize):
    class _ParentClass:

        def __init__(self, *args, **kwargs):
            return  # noqa

        def run(self, *args, **kwargs):  # noqa
            return {}

    params, expected_result = params_set_child_with_children
    instance = action_module(ActionModule)
    instance._task.args = params

    with patch.object(instance, 'validate_parameters', return_value=True):
        with patch('ansible_collections.datadope.discovery.plugins.action.software_facts.super') as mock_super:
            mock_super.return_value = _ParentClass()
            result = instance.run(None, task_vars)

    assert 'ansible_facts' in result
    assert 'software' in result['ansible_facts']
    assert normalize(result['ansible_facts']['software']) == normalize(expected_result)


@pytest.mark.parametrize(
    ('original_list', 'include', 'exclude', 'expected_list'),
    (
            (
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3"), dict(name="SW 4"), dict(name="SW 5")],
                    ['SW 1', 'SW 2', 'SW 3'],
                    ['SW 3'],
                    [dict(name="SW 1"), dict(name="SW 2")]
            ),
            (
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3"), dict(name="SW 4"), dict(name="SW 5")],
                    ['all'],
                    ['SW 3'],
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 4"), dict(name="SW 5")]
            ),
            (
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3"), dict(name="SW 4"), dict(name="SW 5")],
                    None,
                    ['SW 3'],
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 4"), dict(name="SW 5")]
            ),
            (
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3"), dict(name="SW 4"), dict(name="SW 5")],
                    ['SW 1', 'SW 2', 'SW 3'],
                    [],
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3")]
            ),
            (
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3"), dict(name="SW 4"), dict(name="SW 5")],
                    ['SW 1', 'SW 2', 'SW 3'],
                    None,
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3")]
            ),
            (
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3"), dict(name="SW 4"), dict(name="SW 5")],
                    None,
                    None,
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3"), dict(name="SW 4"), dict(name="SW 5")]
            ),
            (
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3"), dict(name="SW 4"), dict(name="SW 5")],
                    [],
                    None,
                    []
            ),
            (
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3"), dict(name="SW 4"), dict(name="SW 5")],
                    'remove',
                    'remove',
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3"), dict(name="SW 4"), dict(name="SW 5")]
            ),
            (
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3"), dict(name="SW 4"), dict(name="SW 5")],
                    ['SW 1', 'SW 2', 'SW 3'],
                    'remove',
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3")]
            ),
            (
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 3"), dict(name="SW 4"), dict(name="SW 5")],
                    'remove',
                    ['SW 3'],
                    [dict(name="SW 1"), dict(name="SW 2"), dict(name="SW 4"), dict(name="SW 5")]
            )
    )
)
def test_include_exclude(action_module, task_vars, original_list, include, exclude, expected_list):
    params = {
        'software_list': original_list,
        'include_software': include,
        'exclude_software': exclude,
        'processes': [],
        'tcp_listen': [],
        'udp_listen': [],
        'packages': {},
        'dockers': {}
    }
    if params['include_software'] == 'remove':
        del params['include_software']
    if params['exclude_software'] == 'remove':
        del params['exclude_software']

    class _ParentClass:

        def __init__(self, *args, **kwargs):
            return  # noqa

        def run(self, *args, **kwargs):  # noqa
            return {}

    instance = action_module(ActionModule)
    instance._task.args = params

    with patch.object(instance, 'validate_parameters', return_value=True):
        with patch('ansible_collections.datadope.discovery.plugins.action.software_facts.super') as mock_super:
            mock_super.return_value = _ParentClass()
            with patch.object(instance, 'process_software') as mocked_process_software:
                instance.run(None, task_vars)

    mocked_process_software.assert_called_once_with(
        software_list=expected_list,
        processes=[],
        tcp_listen=[],
        udp_listen=[],
        packages={},
        dockers={},
        task_vars=task_vars,
        pre_tasks=None,
        post_tasks=None)


@pytest.mark.parametrize(argnames=['params_and_expected_result'],
                         argvalues=[
                             ('params_set_child_with_children',),
                             ('params_set_child_without_children',),
                             ('params_set_parent_with_children',),
                             ('params_set_parent_without_children',),
                             ('params_set_dockers_with_children',),
                             ('params_set_dockers_without_children',)]
                         )
def test_get_software_ok(action_module, normalize, params_and_expected_result, request):
    params_and_expected_result = request.getfixturevalue(params_and_expected_result)
    params, expected_result = params_and_expected_result
    result = action_module(ActionModule).process_software(**params)
    assert normalize(result) == normalize(expected_result)


def test_plugins_empty_list(action_module, params_set_child_without_children, normalize):
    params, expected_result = params_set_child_without_children
    params['software_list'][0]['custom_tasks'] = []
    _action_module = action_module(ActionModule)
    mocked_task_vars = MagicMock()
    with patch.object(_action_module, '_execute_plugin') as mocked_execute_plugin:
        result = _action_module.process_software(task_vars=mocked_task_vars, **params)
    mocked_execute_plugin.assert_not_called()
    mocked_task_vars.__setitem__.assert_called_once_with('__instance__', ANY)
    assert normalize(result) == normalize(expected_result)


def test_plugins_one_plugin(action_module, params_set_child_without_children, normalize):
    params, expected_result = params_set_child_without_children
    the_plugin = {
        'name': 'the name',
        'the_plugin': {}
    }
    params['software_list'][0]['custom_tasks'] = [the_plugin]
    _action_module = action_module(ActionModule)
    with patch.object(_action_module, '_execute_plugin') as mocked_execute_plugin:
        result = _action_module.process_software(**params)
    mocked_execute_plugin.assert_called_once_with(the_plugin, expected_result[0], {})
    assert normalize(result) == normalize(expected_result)


def test_plugins_one_plugin_args_as_list(action_module, params_set_child_without_children, normalize):
    params, expected_result = params_set_child_without_children
    the_plugin = {
        'name': 'the name',
        'the_plugin': []
    }
    params['software_list'][0]['custom_tasks'] = [the_plugin]
    _action_module = action_module(ActionModule)
    with patch.object(_action_module, '_execute_plugin') as mocked_execute_plugin:
        result = _action_module.process_software(**params)
    mocked_execute_plugin.assert_called_once_with(the_plugin, expected_result[0], {})
    assert normalize(result) == normalize(expected_result)


@pytest.mark.parametrize(
    ('plugin_def', 'wrong_attribute'),
    [
        (
                {
                    'name': 'the name',
                    'the_plugin': [],
                    'unsupported': 'value'
                }, 'unsupported'
        ),
        (
                {
                    'name': 'the name',
                    'the_plugin': 'a text',
                    'when': 'yes'
                }, 'the_plugin'
        )
    ]
)
def test_plugins_wrong_plugin_definition(action_module, params_set_child_without_children, plugin_def, wrong_attribute):
    params, expected_result = params_set_child_without_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    with pytest.raises(AnsibleRuntimeError) as ex_info:
        _action_module.process_software(**params)
    assert ex_info.value.message == "Unsupported attribute '{0}' for plugin definition '{1}'" \
        .format(wrong_attribute, plugin_def)


def test_plugins_two_plugins(action_module, params_set_child_without_children, normalize):
    params, expected_result = params_set_child_without_children
    the_plugin1 = {
        'name': 'the name 1',
        'the_plugin1': {}
    }
    the_plugin2 = {
        'name': 'the name 2',
        'the_plugin2': {}
    }
    params['software_list'][0]['custom_tasks'] = [the_plugin1, the_plugin2]
    _action_module = action_module(ActionModule)
    with patch.object(_action_module, '_execute_plugin') as mocked_execute_plugin:
        result = _action_module.process_software(**params)
    assert mocked_execute_plugin.call_count == 2
    mocked_execute_plugin.assert_has_calls(calls=[
        call(the_plugin1, expected_result[0], {}),
        call(the_plugin2, expected_result[0], {})
    ])
    assert normalize(result) == normalize(expected_result)


def test_plugins_condition_false(action_module, params_set_child_without_children):
    params, expected_result = params_set_child_without_children
    the_plugin = {
        'name': 'the name',
        'the_plugin': {
            'arg1': 'val1',
            'arg2': 'val2'
        },
        'when': 'False'
    }
    params['software_list'][0]['custom_tasks'] = [the_plugin]
    _action_module = action_module(ActionModule)
    mocked_templar = _action_module._templar
    mocked_templar.available_variables = {}
    mocked_plugin = MagicMock()
    task_vars = {}
    params['task_vars'] = task_vars
    with patch.object(_action_module, '_get_software_facts_plugin') as mocked_get_software_facts_plugin:
        mocked_get_software_facts_plugin.return_value = mocked_plugin
        with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
            mocked_check_conditions.return_value = False
            _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    mocked_get_software_facts_plugin.assert_called_once_with('the_plugin', _action_module, task_vars, 'the name')
    assert task_vars == {
        '__instance__': expected_result[0]
    }
    mocked_check_conditions.assert_called_once_with("False", task_vars)


def test_plugins_condition_loop_one_false(action_module, params_set_child_without_children):
    params, expected_result = params_set_child_without_children
    the_plugin = {
        'name': 'the name',
        'the_plugin': {
            'arg1': 'val1',
            'arg2': 'val2'
        },
        'when': '__item__ == "item1"',
        'loop': ['item1', 'item2']
    }
    params['software_list'][0]['custom_tasks'] = [the_plugin]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars
    mocked_plugin = MagicMock()
    mocked_plugin.run.return_value = {'item_value': 'item2'}
    with patch.object(_action_module, '_get_software_facts_plugin') as mocked_get_software_facts_plugin:
        mocked_get_software_facts_plugin.return_value = mocked_plugin
        with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
            with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
                with patch.object(_action_module, '_store_plugin_result', return_value=None):
                    mocked_check_conditions.side_effect = [False, True]
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    mocked_get_software_facts_plugin.assert_called_once_with('the_plugin', _action_module, task_vars, 'the name')
    assert task_vars == {
        '__instance__': expected_result[0],
        '__item__': 'item2',
    }
    assert mocked_check_conditions.call_count == 2


def test_plugins_non_existing(action_module, params_set_child_without_children):
    plugin_def = {
        'name': 'the name',
        'non_existing_plugin': [],
        'when': 'yes'
    }
    params, expected_result = params_set_child_without_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    mocked_templar = _action_module._templar
    mocked_templar.available_variables = {}
    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        mocked_check_conditions.return_value = True
        with pytest.raises(AnsibleRuntimeError) as ex_info:
            _action_module.process_software(**params)
    assert ex_info.value.message == "Software Facts plugin {0} not found" \
        .format('non_existing_plugin')


@pytest.mark.parametrize(
    argnames=('plugin_def', 'plugin_result'),
    argvalues=(
            (
                    {
                        'name': 'the name',
                        'the_plugin': {'arg1': 'val1', 'arg2': 'val2'},
                        'when': 'yes'
                    }, {'k1', 'val1'}
            ),
            (
                    {
                        'the_plugin': {'arg1': 'val1', 'arg2': 'val2'},
                        'when': 'yes'
                    }, None
            )
    )
)
def test_plugins_result_ok(action_module, params_set_child_without_children, plugin_def, plugin_result):
    params, expected_result = params_set_child_without_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars
    mocked_plugin = MagicMock()
    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                mocked_check_conditions.return_value = True
                with patch.object(_action_module, '_get_software_facts_plugin') as mocked_get_software_facts_plugin:
                    mocked_get_software_facts_plugin.return_value = mocked_plugin
                    mocked_plugin.validate_args.return_value = plugin_def['the_plugin']
                    mocked_plugin.run.return_value = plugin_result
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    mocked_get_software_facts_plugin.assert_called_once_with('the_plugin', _action_module, task_vars,
                                                             plugin_def.get('name', 'the_plugin'))
    mocked_plugin.validate_args.assert_called_once_with({'arg1': 'val1', 'arg2': 'val2'})
    mocked_plugin.run.assert_called_once_with({'arg1': 'val1', 'arg2': 'val2'},
                                              {'when': 'yes'},
                                              expected_result[0])
    assert task_vars == {
        '__instance__': expected_result[0]
    }


def test_plugins_result_error(action_module, params_set_child_with_children):
    plugin_def = {
        'name': 'the name',
        'the_plugin': {'arg1': 'val1', 'arg2': 'val2'},
        'when': 'yes'
    }
    error_message = 'The error message'
    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars
    mocked_plugin = MagicMock()
    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                mocked_check_conditions.return_value = True
                with patch.object(_action_module, '_get_software_facts_plugin') as mocked_get_software_facts_plugin:
                    mocked_get_software_facts_plugin.return_value = mocked_plugin
                    mocked_plugin.validate_args.return_value = plugin_def['the_plugin']
                    mocked_plugin.run.side_effect = Exception(error_message)
                    with pytest.raises(Exception) as excinfo:
                        _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    mocked_get_software_facts_plugin.assert_called_once_with('the_plugin', _action_module, task_vars,
                                                             plugin_def.get('name'))
    mocked_plugin.validate_args.assert_called_once_with({'arg1': 'val1', 'arg2': 'val2'})
    mocked_plugin.run.assert_called_once_with({'arg1': 'val1', 'arg2': 'val2'},
                                              {'when': 'yes'},
                                              expected_result[0])
    assert str(excinfo.value) == error_message


def test_plugins_result_error_ignore_errors(action_module, params_set_child_with_children):
    plugin_def = {
        'name': 'the name',
        'the_plugin': {'arg1': 'val1', 'arg2': 'val2'},
        'when': 'yes',
        'ignore_errors': 'yes'
    }
    error_message = 'The error message'
    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars
    mocked_plugin = MagicMock()
    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                mocked_check_conditions.return_value = True
                with patch.object(_action_module, '_get_software_facts_plugin') as mocked_get_software_facts_plugin:
                    mocked_get_software_facts_plugin.return_value = mocked_plugin
                    mocked_plugin.validate_args.return_value = plugin_def['the_plugin']
                    mocked_plugin.run.side_effect = Exception(error_message)
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    mocked_get_software_facts_plugin.assert_called_once_with('the_plugin', _action_module, task_vars,
                                                             plugin_def.get('name'))
    mocked_plugin.validate_args.assert_called_once_with({'arg1': 'val1', 'arg2': 'val2'})
    mocked_plugin.run.assert_called_once_with({'arg1': 'val1', 'arg2': 'val2'},
                                              {'when': 'yes', 'ignore_errors': 'yes'},
                                              expected_result[0])
    assert task_vars['__instance__'] == expected_result[0]


def test_plugins_loop(action_module, params_set_child_without_children):
    plugin_def = {
        'name': 'the name',
        'the_plugin': {'arg1': '<< __item__ >>', 'arg2': 'val2'},
        'when': 'yes',
        'loop': ['item1', 'item2']
    }
    elements = plugin_def['loop'].copy()

    def _replace_vars(data):
        if isinstance(data, dict):
            result = data.copy()
            if 'arg1' in data:
                result['arg1'] = elements.pop(0)
            return result
        return data

    params, expected_result = params_set_child_without_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars
    mocked_plugin = MagicMock()
    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', _replace_vars):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                mocked_check_conditions.return_value = True
                with patch.object(_action_module, '_get_software_facts_plugin') as mocked_get_software_facts_plugin:
                    mocked_get_software_facts_plugin.return_value = mocked_plugin
                    mocked_plugin.validate_args.side_effect = [{'arg1': x, 'arg2': 'val2'} for x in plugin_def['loop']]
                    mocked_plugin.run.side_effect = [{'item_value': x} for x in plugin_def['loop']]
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    mocked_get_software_facts_plugin.assert_called_once_with('the_plugin', _action_module, task_vars,
                                                             plugin_def.get('name'))
    assert mocked_plugin.validate_args.call_count == 2
    mocked_plugin.validate_args.assert_has_calls([call({'arg1': x, 'arg2': 'val2'}) for x in plugin_def['loop']])
    assert mocked_plugin.run.call_count == 2
    mocked_plugin.run.assert_has_calls([call({'arg1': x, 'arg2': 'val2'},
                                             {'when': 'yes', 'loop': ['item1', 'item2']},
                                             expected_result[0]) for x in plugin_def['loop']])
    assert task_vars == {
        '__instance__': expected_result[0],
        '__item__': 'item2'
    }


def test_plugins_loop_loop_var(action_module, params_set_child_without_children):
    plugin_def = {
        'name': 'the name',
        'the_plugin': {'arg1': '<< __other_item__ >>', 'arg2': 'val2'},
        'when': 'yes',
        'loop': ['item1', 'item2'],
        'loop_control': {'loop_var': '__other_item__'}
    }
    elements = plugin_def['loop'].copy()

    def _replace_vars(data):
        if isinstance(data, dict):
            result = data.copy()
            if 'arg1' in data:
                result['arg1'] = elements.pop(0)
            return result
        return data

    params, expected_result = params_set_child_without_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars
    mocked_plugin = MagicMock()
    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', _replace_vars):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                mocked_check_conditions.return_value = True
                with patch.object(_action_module, '_get_software_facts_plugin') as mocked_get_software_facts_plugin:
                    mocked_get_software_facts_plugin.return_value = mocked_plugin
                    mocked_plugin.validate_args.return_value = plugin_def['the_plugin']
                    mocked_plugin.validate_args.side_effect = [{'arg1': x, 'arg2': 'val2'} for x in plugin_def['loop']]
                    mocked_plugin.run.side_effect = [{'item_value': x} for x in plugin_def['loop']]
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    mocked_get_software_facts_plugin.assert_called_once_with('the_plugin', _action_module, task_vars,
                                                             plugin_def.get('name'))
    assert mocked_plugin.validate_args.call_count == 2
    mocked_plugin.validate_args.assert_has_calls([call({'arg1': x, 'arg2': 'val2'}) for x in plugin_def['loop']])
    assert mocked_plugin.run.call_count == 2
    mocked_plugin.run.assert_has_calls([call({'arg1': x, 'arg2': 'val2'},
                                             {'when': 'yes', 'loop': ['item1', 'item2'],
                                              'loop_control': {'loop_var': '__other_item__'}},
                                             expected_result[0]) for x in plugin_def['loop']])
    assert task_vars == {
        '__instance__': expected_result[0],
        '__other_item__': 'item2'
    }


def test_plugins_loop_error_first(action_module, params_set_child_with_children):
    plugin_def = {
        'name': 'the name',
        'the_plugin': {'arg1': '<< __item__ >>', 'arg2': 'val2'},
        'when': 'yes',
        'loop': ['item1', 'item2']
    }
    elements = plugin_def['loop'].copy()

    def _replace_vars(data):
        if isinstance(data, dict):
            result = data.copy()
            if 'arg1' in data:
                result['arg1'] = elements.pop(0)
            return result
        return data

    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars
    mocked_plugin = MagicMock()
    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', _replace_vars):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                mocked_check_conditions.return_value = True
                with patch.object(_action_module, '_get_software_facts_plugin') as mocked_get_software_facts_plugin:
                    mocked_get_software_facts_plugin.return_value = mocked_plugin
                    mocked_plugin.validate_args.side_effect = [{'arg1': x, 'arg2': 'val2'} for x in plugin_def['loop']]
                    mocked_plugin.run.side_effect = [Exception("the error message"), {'item_value': 'item2'}]
                    with pytest.raises(Exception) as exinfo:
                        _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    assert str(exinfo.value) == "the error message"
    mocked_get_software_facts_plugin.assert_called_once_with('the_plugin', _action_module, task_vars,
                                                             plugin_def.get('name'))
    assert mocked_plugin.validate_args.call_count == 1
    mocked_plugin.validate_args.assert_has_calls([call({'arg1': 'item1', 'arg2': 'val2'})])
    assert mocked_plugin.run.call_count == 1
    mocked_plugin.run.assert_has_calls([call({'arg1': 'item1', 'arg2': 'val2'},
                                             {'when': 'yes', 'loop': ['item1', 'item2']},
                                             expected_result[0])])
    assert task_vars == {
        '__instance__': expected_result[0],
        '__item__': 'item1'
    }


def test_plugins_loop_error_second(action_module, params_set_child_with_children):
    plugin_def = {
        'name': 'the name',
        'the_plugin': {'arg1': '<< __item__ >>', 'arg2': 'val2'},
        'when': 'yes',
        'loop': ['item1', 'item2']
    }
    elements = plugin_def['loop'].copy()

    def _replace_vars(data):
        if isinstance(data, dict):
            result = data.copy()
            if 'arg1' in data:
                result['arg1'] = elements.pop(0)
            return result
        return data

    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars
    mocked_plugin = MagicMock()
    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', _replace_vars):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                mocked_check_conditions.return_value = True
                with patch.object(_action_module, '_get_software_facts_plugin') as mocked_get_software_facts_plugin:
                    mocked_get_software_facts_plugin.return_value = mocked_plugin
                    mocked_plugin.validate_args.side_effect = [{'arg1': x, 'arg2': 'val2'} for x in plugin_def['loop']]
                    mocked_plugin.run.side_effect = [{'item_value': 'item1'}, Exception('the error message')]
                    with pytest.raises(Exception) as exinfo:
                        _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    assert str(exinfo.value) == 'the error message'
    mocked_get_software_facts_plugin.assert_called_once_with('the_plugin', _action_module, task_vars,
                                                             plugin_def.get('name'))
    assert mocked_plugin.validate_args.call_count == 2
    mocked_plugin.validate_args.assert_has_calls([call({'arg1': x, 'arg2': 'val2'}) for x in plugin_def['loop']])
    assert mocked_plugin.run.call_count == 2
    mocked_plugin.run.assert_has_calls([call({'arg1': x, 'arg2': 'val2'},
                                             {'when': 'yes', 'loop': ['item1', 'item2']},
                                             expected_result[0]) for x in plugin_def['loop']])
    assert task_vars == {
        '__instance__': expected_result[0],
        '__item__': 'item2'
    }


def test_plugins_loop_error_both_ignored(action_module, params_set_child_without_children):
    plugin_def = {
        'name': 'the name',
        'the_plugin': {'arg1': '<< __item__ >>', 'arg2': 'val2'},
        'when': 'yes',
        'loop': ['item1', 'item2'],
        'ignore_errors': 'yes'
    }
    elements = elements = plugin_def['loop'].copy()

    def _replace_vars(data):
        if isinstance(data, dict):
            result = data.copy()
            if 'arg1' in data:
                result['arg1'] = elements.pop(0)
            return result
        return data

    params, expected_result = params_set_child_without_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars
    mocked_plugin = MagicMock()
    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', _replace_vars):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                mocked_check_conditions.return_value = True
                with patch.object(_action_module, '_get_software_facts_plugin') as mocked_get_software_facts_plugin:
                    mocked_get_software_facts_plugin.return_value = mocked_plugin
                    mocked_plugin.validate_args.side_effect = [{'arg1': x, 'arg2': 'val2'} for x in plugin_def['loop']]
                    mocked_plugin.run.side_effect = [Exception('the first error message'),
                                                     Exception('the second error message')]
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    mocked_get_software_facts_plugin.assert_called_once_with('the_plugin', _action_module, task_vars,
                                                             plugin_def.get('name'))
    assert mocked_plugin.validate_args.call_count == 2
    mocked_plugin.validate_args.assert_has_calls([call({'arg1': x, 'arg2': 'val2'}) for x in plugin_def['loop']])
    assert mocked_plugin.run.call_count == 2
    mocked_plugin.run.assert_has_calls([call({'arg1': x, 'arg2': 'val2'},
                                             {'when': 'yes', 'loop': ['item1', 'item2'], 'ignore_errors': 'yes'},
                                             expected_result[0]) for x in plugin_def['loop']])
    assert task_vars == {
        '__instance__': expected_result[0],
        '__item__': 'item2'
    }


@pytest.mark.parametrize(
    argnames=('plugin_def', 'error_message'),
    argvalues=(
            (
                    {
                        'name': 'the name',
                        'block': {},
                        'when': 'yes'
                    }, "'block' plugin 'the name' needs a list of plugins as argument"
            ),
            (
                    {
                        'name': 'the name',
                        'block': [
                            {
                                'name': 'the inner name',
                                'the_plugin': {},
                                'when': 'yes'
                            }
                        ],
                        'when': 'yes'
                    }, "Exception executing plugin 'the inner name'"
            )
    )
)
def test_plugins_block_error(action_module, params_set_child_with_children,
                             plugin_def, error_message):
    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars

    original_execute_plugin = _action_module._execute_plugin

    def pathed_execute_plugin(*args, **kwargs):
        arg = kwargs.get('plugin', args[0])
        if 'block' in arg:
            return original_execute_plugin(*args, **kwargs)
        raise AnsibleRuntimeError(message="Exception executing plugin 'the inner name'")

    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                with patch.object(_action_module, '_execute_plugin', new=pathed_execute_plugin):
                    mocked_check_conditions.return_value = True
                    with pytest.raises(AnsibleRuntimeError) as exinfo:
                        _action_module.process_software(**params)

    assert exinfo.value.message == error_message
    assert task_vars == {
        '__instance__': expected_result[0]
    }


def test_plugins_block(action_module, params_set_child_with_children):
    plugin_def = {
        'name': 'the name',
        'block': [
            {
                'name': 'the inner name 1',
                'the_plugin_1': {},
                'when': 'yes'
            },
            {
                'name': 'the inner name 2',
                'the_plugin_2': {},
                'when': 'yes'
            }
        ],
        'when': 'yes'
    }
    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars

    original_execute_plugin = _action_module._execute_plugin

    _executions = {'number': 0}  # As dict because python 2 does not support nonlocal

    def pathed_execute_plugin(*args, **kwargs):
        _executions['number'] += 1
        arg = kwargs.get('plugin', args[0])
        if 'block' in arg:
            return original_execute_plugin(*args, **kwargs)
        return {arg['name']: 'ok'}

    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                with patch.object(_action_module, '_execute_plugin', new=pathed_execute_plugin):
                    mocked_check_conditions.return_value = True
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    assert _executions['number'] == 3

    assert task_vars == {
        '__instance__': expected_result[0]
    }


def test_plugins_block_with_loop(action_module, params_set_child_with_children):
    plugin_def = {
        'name': 'the name',
        'block': [
            {
                'name': 'the inner name 1',
                'the_plugin_1': {},
                'when': 'yes'
            },
            {
                'name': 'the inner name 2',
                'the_plugin_2': {},
                'when': 'yes'
            }
        ],
        'when': 'yes',
        'loop': ['item1', 'item2']
    }
    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars

    original_execute_plugin = _action_module._execute_plugin

    _executions = {'number': 0}  # As dict because python 2 does not support nonlocal

    def pathed_execute_plugin(*args, **kwargs):
        _executions['number'] += 1
        arg = kwargs.get('plugin', args[0])
        if 'block' in arg:
            return original_execute_plugin(*args, **kwargs)
        return {arg['name']: 'ok'}

    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                with patch.object(_action_module, '_execute_plugin', new=pathed_execute_plugin):
                    mocked_check_conditions.return_value = True
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    assert _executions['number'] == 5

    assert task_vars == {
        '__instance__': expected_result[0],
        '__item__': 'item2'
    }


def test_plugins_block_with_loop_in_loop(action_module, params_set_child_with_children):
    plugin_def = {
        'name': 'the name',
        'block': [
            {
                'name': 'the inner name 1',
                'the_plugin_1': {},
                'when': 'yes',
                'loop': ['inner1', 'inner2'],
                'loop_control': {'loop_var': '__inner_item__'}
            },
            {
                'name': 'the inner name 2',
                'the_plugin_2': {},
                'when': 'yes'
            }
        ],
        'when': 'yes',
        'loop': ['item1', 'item2']
    }
    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars

    _executions = {'number': 0}  # As dict because python 2 does not support nonlocal

    mocked_plugin = MagicMock()
    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                mocked_check_conditions.return_value = True
                with patch.object(_action_module, '_get_software_facts_plugin') as mocked_get_software_facts_plugin:
                    mocked_get_software_facts_plugin.return_value = mocked_plugin
                    mocked_plugin.validate_args.return_value = None
                    mocked_plugin.run.return_value = 'ok'
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    # assert _executions['number'] == 5

    assert task_vars == {
        '__instance__': expected_result[0],
        '__item__': 'item2',
        '__inner_item__': 'inner2'
    }


def test_plugins_block_plugin_error(action_module, params_set_child_with_children):
    plugin_def = {
        'name': 'the name',
        'block': [
            {
                'name': 'the inner name 1',
                'the_plugin_1': {},
                'when': 'yes'
            }
        ],
        'when': 'yes'
    }
    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars

    original_execute_plugin = _action_module._execute_plugin

    def pathed_execute_plugin(*args, **kwargs):
        arg = kwargs.get('plugin', args[0])
        if 'block' in arg:
            return original_execute_plugin(*args, **kwargs)
        raise AnsibleRuntimeError(message="Exception executing plugin 'the inner name'")

    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                with patch.object(_action_module, '_execute_plugin', new=pathed_execute_plugin):
                    mocked_check_conditions.return_value = True
                    with pytest.raises(AnsibleRuntimeError) as exinfo:
                        _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    assert exinfo.value.message == "Exception executing plugin 'the inner name'"
    assert task_vars == {
        '__instance__': expected_result[0]
    }


def test_plugins_block_ignore_errors(action_module, params_set_child_with_children):
    plugin_def = {
        'name': 'the name',
        'block': [
            {
                'name': 'the inner name 1',
                'the_plugin_1': {},
                'when': 'yes'
            }
        ],
        'when': 'yes',
        'ignore_errors': 'yes'
    }
    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars

    original_execute_plugin = _action_module._execute_plugin

    def pathed_execute_plugin(*args, **kwargs):
        arg = kwargs.get('plugin', args[0])
        if 'block' in arg:
            return original_execute_plugin(*args, **kwargs)
        raise AnsibleRuntimeError(message="Exception executing plugin 'the inner name'")

    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                with patch.object(_action_module, '_execute_plugin', new=pathed_execute_plugin):
                    mocked_check_conditions.return_value = True
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    assert task_vars == {
        '__instance__': expected_result[0]
    }


@pytest.mark.parametrize(
    ('conditions', 'expected_result'),
    (
            ('True (as string)', True),
            ('False (as string)', False),
            (['True 1', 'True 2'], True),
            (['True 1', 'False 2'], False),
            (['False 1', 'True 2'], False),
            (['False 1', 'False 2'], False)
    )
)
def test_plugin_conditions(action_module, conditions, expected_result):
    class MockedConditional:
        def __init__(self, expected_templar, expected_vars):
            self.when = None
            self.expected_templar = expected_templar
            self.expected_vars = expected_vars

        def evaluate_conditional(self, templar, all_vars):
            assert isinstance(self.when, list) and len(self.when) == 1, "Wrong when"
            assert templar == self.expected_templar, "Wrong templar"
            assert all_vars == self.expected_vars, "Wrong vars"
            return True if 'true' in self.when[0].lower() else False

    mocked_vars = {'var1': 'val1', 'var2': 'val2'}
    _action_module = action_module(ActionModule)
    mocked_templar = _action_module._templar
    mocked_templar.available_variables = {}
    mocked_conditional = MockedConditional(_action_module._templar, mocked_vars)
    _action_module._conditional = mocked_conditional
    result = _action_module._check_conditions(conditions, mocked_vars)
    assert result == expected_result


@pytest.mark.parametrize(
    ('variables', 'expected_result'),
    (
            ('untemplated', 'untemplated'),
            ('<< var1 >>', 'value1'),
            (
                    {
                        'key1': 'untemplated',
                        'key2': '<< var1 >>',
                        'key3': '<< var2 >>',
                    },
                    {
                        'key1': 'untemplated',
                        'key2': 'value1',
                        'key3': 'value2',
                    }
            ),
            (
                    [
                        'untemplated',
                        '<< var1 >>',
                        '<< var2 >>'
                    ],
                    [
                        'untemplated',
                        'value1',
                        'value2'
                    ]
            ),
            (1, 1),
            (1.5, 1.5),
            (b'Hola', 'Hola')
    )
)
def test_replace_vars(action_module, variables, expected_result):
    var_replacements = {
        '{{ var1 }}': 'value1',
        '{{ var2 }}': 'value2'
    }

    def mocked_template(data, **kwargs):
        if _TEMPLAR_HAS_TEMPLATE_CACHE:
            assert 'cache' in kwargs and kwargs['cache'] is False, "Wrong template cache parameter"
        if isinstance(data, dict):
            new_dict = {}
            for k, v in iteritems(data):
                new_dict[k] = mocked_template(v)
            return new_dict
        elif isinstance(data, dict):
            new_list = []
            for element in data:
                new_list.append(mocked_template(element))
            return new_list
        else:
            return var_replacements.get(data, data)

    _action_module = action_module(ActionModule)
    mocked_templar = _action_module._templar
    mocked_templar.template = mocked_template

    result = _action_module._replace_instance_vars(variables)

    assert result == expected_result


def test_storage_plugin_result(action_module):
    attributes = {'register': 'the_var'}
    task_vars = {}
    plugin_result = {'failed': False, 'result': 'the result'}
    _action_module = action_module(ActionModule)
    with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
        _action_module._store_plugin_result(attributes, task_vars, plugin_result)

    assert task_vars == {'the_var': plugin_result}


def test_storage_plugin_result_bad_key(action_module):
    attributes = {'register': 'the_var.invalid'}
    task_vars = {}
    plugin_result = {'failed': False, 'result': 'the result'}
    _action_module = action_module(ActionModule)
    with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            _action_module._store_plugin_result(attributes, task_vars, plugin_result)

    assert task_vars == {}
    assert exinfo.value.message == "Invalid variable name in 'register' specified: 'the_var.invalid'"


def test_storage_plugin_result_no_register(action_module):
    attributes = {'other': 'the_value'}
    task_vars = {}
    plugin_result = {'failed': False, 'result': 'the result'}
    _action_module = action_module(ActionModule)
    with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
        _action_module._store_plugin_result(attributes, task_vars, plugin_result)

    assert task_vars == {}


def test_plugins_include_tasks(action_module, params_set_child_with_children):
    plugin_def = {
        'name': 'the name',
        'include_tasks': {
            'file': os.path.join(os.path.dirname(__file__), 'test_include_tasks.yaml')
        }
    }
    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars

    original_execute_plugin = _action_module._execute_plugin

    _executions = {'number': 0}  # As dict because python 2 does not support nonlocal

    def pathed_execute_plugin(*args, **kwargs):
        _executions['number'] += 1
        arg = kwargs.get('plugin', args[0])
        if 'include_tasks' in arg:
            return original_execute_plugin(*args, **kwargs)
        return {arg['name']: 'ok'}

    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                with patch.object(_action_module, '_execute_plugin', new=pathed_execute_plugin):
                    mocked_check_conditions.return_value = True
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    assert _executions['number'] == 3

    assert task_vars == {
        '__instance__': expected_result[0]
    }


def test_plugins_include_tasks_no_file(action_module, params_set_child_with_children):
    plugin_def = {
        'name': 'the name',
        'include_tasks': {
            'other': os.path.join(os.path.dirname(__file__), 'test_include_tasks.yaml')
        }
    }
    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars

    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                with pytest.raises(AnsibleRuntimeError) as exinfo:
                    mocked_check_conditions.return_value = True
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    assert exinfo.value.message == "Missing argument 'file' for 'include_tasks' plugin 'the name'"

    assert task_vars == {
        '__instance__': expected_result[0]
    }


def test_plugins_include_tasks_bad_file(action_module, params_set_child_with_children):
    plugin_def = {
        'name': 'the name',
        'include_tasks': {
            'file': __file__
        }
    }
    params, expected_result = params_set_child_with_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    _action_module = action_module(ActionModule)
    task_vars = {}
    params['task_vars'] = task_vars

    with patch.object(_action_module, '_check_conditions') as mocked_check_conditions:
        with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
            with patch.object(_action_module, '_store_plugin_result', return_value=None):
                with pytest.raises(AnsibleRuntimeError) as exinfo:
                    mocked_check_conditions.return_value = True
                    _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    assert exinfo.value.message.startswith("Cannot read file '{0}' for 'include_tasks' plugin 'the name':"
                                           .format(__file__))

    assert task_vars == {
        '__instance__': expected_result[0]
    }


@pytest.mark.parametrize(
    ('plugin_def', 'plugin_result', 'expected_var'),
    (
            (
                    dict(name='the name', the_plugin={}, register='the_var'),
                    'string',
                    dict(task='the name', result='string', failed=False, skipped=False, msg='',
                         invocation={'plugin_args': {}, 'plugin_name': 'the_plugin'})
            ),
            (
                    dict(name='the name', the_plugin={}, register='the_var'),
                    dict(failed=True, msg='The error message'),
                    dict(task='the name', failed=True, skipped=False, msg='The error message',
                         invocation={'plugin_args': {}, 'plugin_name': 'the_plugin'})
            ),
            (
                    dict(name='the name', the_plugin={}, register='the_var', loop=['item1', 'item2']),
                    'string',
                    dict(task='the name', msg='All items completed', results=[
                        dict(result='string', failed=False, skipped=False, msg='', __item__='item1',
                             invocation={'plugin_args': {}, 'plugin_name': 'the_plugin'}),
                        dict(result='string', failed=False, skipped=False, msg='', __item__='item2',
                             invocation={'plugin_args': {}, 'plugin_name': 'the_plugin'})
                    ])
            ),
            (
                    dict(name='the name', the_plugin={}, register='the_var',
                         loop=['item1', 'item2'], loop_control=dict(loop_var='the_loop_var')),
                    'string',
                    dict(task='the name', msg='All items completed', results=[
                        dict(result='string', failed=False, skipped=False, msg='', the_loop_var='item1',
                             invocation={'plugin_args': {}, 'plugin_name': 'the_plugin'}),
                        dict(result='string', failed=False, skipped=False, msg='', the_loop_var='item2',
                             invocation={'plugin_args': {}, 'plugin_name': 'the_plugin'})
                    ])
            ),
            (
                    dict(name='the name', the_plugin={}, register='the_var', ignore_errors=True),
                    AnsibleRuntimeError("The error message"),
                    dict(task='the name', failed=True, skipped=False, msg='The error message', exception=ANY,
                         invocation={'plugin_args': {}, 'plugin_name': 'the_plugin'})
            ),
    )
)
def test_register_plugin(action_module, params_set_child_without_children,
                         plugin_def, plugin_result, expected_var):
    params, expected_result = params_set_child_without_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    task_vars = {}

    _action_module = action_module(ActionModule, task_vars=task_vars)
    mocked_plugin = MagicMock()
    with patch.object(_action_module, '_get_software_facts_plugin', return_value=mocked_plugin):
        if isinstance(plugin_result, Exception):
            mocked_plugin.run.side_effect = plugin_result
        else:
            mocked_plugin.run.return_value = plugin_result
        _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    assert task_vars['__instance__'] == expected_result[0]
    assert task_vars['the_var'] == expected_var


@pytest.mark.parametrize(
    ('plugin_def', 'plugin_name'),
    (
            (
                    dict(name='the name', block=[], register='the_var'), 'block'
            ),
            (
                    dict(name='the name', include_tasks={'file': 'the_file'}, register='the_var'), 'include_tasks'
            )
    )
)
def test_register_plugin_unsupported(action_module, params_set_child_without_children,
                                     plugin_def, plugin_name):
    params, expected_result = params_set_child_without_children
    params['software_list'][0]['custom_tasks'] = [plugin_def]
    task_vars = {}

    with patch('ansible_collections.datadope.discovery.plugins.action.software_facts.display') as mocked_display:
        _action_module = action_module(ActionModule, task_vars=task_vars)
        with patch.object(_action_module, 'get_plugins_from_file', return_value=[]):
            _action_module._execute_plugins(params['software_list'][0], expected_result[0], task_vars)

    mocked_display.warning.assert_called_once_with("Ignoring 'register' attribute for plugin '{0}'".format(plugin_name))

    assert task_vars['__instance__'] == expected_result[0]


@pytest.mark.parametrize(
    ('original_instance', 'plugin_result', 'expected_instance'),
    (
            (
                    dict(var1='value1', var2={'key1': 'v1', 'key2': 'v2'}, var3=[1, 2, 3]),
                    dict(__instance__=dict(var4='value4')),
                    dict(var1='value1', var2={'key1': 'v1', 'key2': 'v2'}, var3=[1, 2, 3], var4='value4')
            ),
            (
                    dict(var1='value1', var2={'key1': 'v1', 'key2': 'v2'}, var3=[1, 2, 3]),
                    dict(__instance__=dict(var2={'key1': 'new1', 'key3': 'v3'}, var3=[4, 5, 6], var4='value4')),
                    dict(var1='value1', var2={'key1': 'new1', 'key2': 'v2', 'key3': 'v3'}, var3=[4, 5, 6],
                         var4='value4')
            ),
            (
                    dict(var1='value1', var2={'key1': 'v1', 'key2': 'v2'}, var3=[1, 2, 3]),
                    dict(__instance__=dict(var2={'key1': 'new1', 'key3': 'v3'}, var3=[4, 5, 6], var4='value4'),
                         __list_merge__='append'),
                    dict(var1='value1', var2={'key1': 'new1', 'key2': 'v2', 'key3': 'v3'}, var3=[1, 2, 3, 4, 5, 6],
                         var4='value4')
            ),
    )
)
def test_plugin_result_instance(action_module, params_set_child_without_children,
                                original_instance, plugin_result, expected_instance):
    params = params_set_child_without_children[0]
    params['software_list'][0]['custom_tasks'] = [dict(name='the name', the_plugin={})]
    task_vars = dict(__instance__=original_instance)

    _action_module = action_module(ActionModule, task_vars=task_vars)
    mocked_plugin = MagicMock()
    with patch.object(_action_module, '_get_software_facts_plugin', return_value=mocked_plugin):
        if isinstance(plugin_result, Exception):
            mocked_plugin.run.side_effect = plugin_result
        else:
            mocked_plugin.run.return_value = plugin_result
        _action_module._execute_plugins(params['software_list'][0], task_vars['__instance__'], task_vars)

    assert task_vars['__instance__'] == expected_instance


@pytest.mark.parametrize(
    ('result', 'conditions', 'expected_result'),
    (
            (
                    dict(failed=True),
                    ['result is failed'],
                    True
            ),
            (
                    dict(failed=False),
                    ['result is failed'],
                    False
            ),
            (
                    dict(),
                    ['result is failed'],
                    False
            ),
            (
                    dict(),
                    ['result is not failed'],
                    True
            ),
            (
                    dict(skipped=True),
                    ['result is skipped'],
                    True
            ),
            (
                    dict(skipped=False),
                    ['result is skipped'],
                    False
            ),
            (
                    dict(),
                    ['result is skipped'],
                    False
            ),
            (
                    dict(),
                    ['result is not skipped'],
                    True
            )
    )
)
def test_condition_is_failed(action_module, result, conditions, expected_result):
    task_vars = dict(result=result)
    _action_module = action_module(ActionModule, task_vars=task_vars)
    assert _action_module._check_conditions(conditions, task_vars) == expected_result


def test_ignore_by_plugin(action_module, params_set_child_with_children):
    plugins = [{
        'set_instance_fact': {
            "NOT_A_REAL_SOFTWARE_REMOVE_FROM_LIST": True
        }
    }]
    params = params_set_child_with_children[0]
    params['software_list'][0]['custom_tasks'] = plugins  # noqa
    _action_module = action_module(ActionModule, task_vars={})
    with patch.object(_action_module, '_replace_instance_vars', lambda x: x):
        result = _action_module.process_software(**params)
    assert result == []
