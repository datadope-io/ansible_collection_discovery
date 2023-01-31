from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible.module_utils.six.moves import builtins  # noqa
from pytest_lazyfixture import lazy_fixture

from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule


@pytest.fixture
def sw_config():
    return {
        "name": "Apache Tomcat Servlet Engine",
        "cmd_regexp": r"\.apache\.tomcat\.startup|\.apache\.catalina\.startup",
        "pkg_regexp": r"tomcat",
        "docker_regexp": r"tomcat(?:-.*):",
        "process_type": "child",
        "return_children": True
    }


@pytest.fixture
def params_set_one_sw(sw_config, read_json_file):
    params = {
        'software_list': [sw_config],
        'processes': read_json_file('resources/oss-devel/processes.json'),
        'dockers': read_json_file('resources/oss-devel/dockers.json')
    }
    params.update(read_json_file('resources/oss-devel/ports.json'))
    expected_result = [{
        "bindings": [{"address": "0.0.0.0",
                      "class": "service",
                      "port": 8443,
                      "protocol": "tcp"}],
        "type": "Apache Tomcat Servlet Engine",
        "discovery_time": "2022-05-26T18:00:00+02:00",
        "process": {
            "children": [
                {
                    "children": [],
                    "cmdline": "/usr/local/openjdk-17/bin/java "
                               "-Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties"
                               " -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Xmx7876m -Xms3846m"
                               " -Djdk.tls.ephemeralDHKeySize=2048"
                               " -Djava.protocol.handler.pkgs=org.apache.catalina.webresources"
                               " -Dorg.apache.catalina.security.SecurityListener.UMASK=0027"
                               " -Xlog:gc=debug:file=logs/gc.log:time,uptime,level,tags:filecount=10,filesize=100m"
                               " -javaagent:/usr/local/tomcat/lib/elastic-apm-agent-1.28.1.jar"
                               " -Delastic.apm.service_name=cmdb"
                               " -Delastic.apm.server_url=http://192.168.8.53:8200 -Delastic.apm.environment=dev"
                               " -Delastic.apm.enabled=true -Delastic.apm.profiling_inferred_spans_enabled=true"
                               " -Delastic.apm.profiling_inferred_spans_min_duration=250ms"
                               " -Delastic.apm.profiling_inferred_spans_included_classes=org.cmdbuild.*"
                               " -Dignore.endorsed.dirs="
                               " -classpath /usr/local/tomcat/bin/bootstrap.jar:/usr/local/tomcat/bin/tomcat-juli.jar"
                               " -Dcatalina.base=/usr/local/tomcat -Dcatalina.home=/usr/local/tomcat"
                               " -Djava.io.tmpdir=/usr/local/tomcat/temp org.apache.catalina.startup.Bootstrap start",
                    "pid": "30748",
                    "ppid": "30709",
                    "user": "root",
                    "cwd": "/usr/local/openjdk-17/bin/"
                }
            ],
            "cmdline": "/bin/sh -c /usr/local/bin/docker-entrypoint.sh catalina.sh run",
            "pid": "30709",
            "ppid": "30689",
            "user": "root",
            "listening_ports": [
                8443
            ],
            "cwd": "/bin/"
        },
        "listening_ports": [8443],
        "version": [
            {
                "type": "docker",
                "number": "0.5.3"
            }
        ],
        "docker": {
            'exposed_ports': {'8080/tcp': {}, '8443/tcp': {}},
            'id': '5a49f7d8a2a4211c508ade8111622a7a26a38a48385ef936382cde0448c5f187',
            "name": "/iometrics-cmdbuild",
            "network_mode": "bridge",
            "image": "nexusregistry.opensolutions.cloud/iometrics-cmdbuild:0.5.3",
            'port_bindings': {'8443/tcp': [{'HostIp': '0.0.0.0',
                                            'HostPort': '8443'}]}
        }
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
        'udp_listen': []
    }
    expected_result = []
    return params, expected_result


@pytest.fixture
def params_set_two_sw(sw_config, params_set_one_sw):
    params_set_one_sw[0]['processes'].append(
        {
            "children": [],
            "cmdline": "/bin/sh -c /usr/local/bin/docker-entrypoint.sh catalina.sh run",
            "cwd": "/bin/",
            "pid": "50709",
            "ppid": "50689",
            "user": "root"
        }
    )
    params_set_one_sw[0]['processes'].append(
        {
            "children": [],
            "cmdline": "/usr/local/openjdk-17/bin/java "
                       "-Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties"
                       " -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Xmx7876m -Xms3846m"
                       " -Djdk.tls.ephemeralDHKeySize=2048"
                       " -Djava.protocol.handler.pkgs=org.apache.catalina.webresources"
                       " -Dorg.apache.catalina.security.SecurityListener.UMASK=0027"
                       " -Xlog:gc=debug:file=logs/gc.log:time,uptime,level,tags:filecount=10,filesize=100m"
                       " -javaagent:/usr/local/tomcat/lib/elastic-apm-agent-1.28.1.jar -Delastic.apm.service_name=cmdb"
                       " -Delastic.apm.server_url=http://192.168.8.53:8200 -Delastic.apm.environment=dev"
                       " -Delastic.apm.enabled=true -Delastic.apm.profiling_inferred_spans_enabled=true"
                       " -Delastic.apm.profiling_inferred_spans_min_duration=250ms"
                       " -Delastic.apm.profiling_inferred_spans_included_classes=org.cmdbuild.*"
                       " -Dignore.endorsed.dirs="
                       " -classpath /usr/local/tomcat/bin/bootstrap.jar:/usr/local/tomcat/bin/tomcat-juli.jar"
                       " -Dcatalina.base=/usr/local/tomcat -Dcatalina.home=/usr/local/tomcat"
                       " -Djava.io.tmpdir=/usr/local/tomcat/temp org.apache.catalina.startup.Bootstrap start",
            "cwd": "/usr/local/openjdk-17/bin/",
            "pid": "50748",
            "ppid": "50709",
            "user": "root"
        }
    )
    params_set_one_sw[0]['tcp_listen'].append(
        {
            "address": "::",
            "name": "tomcat",
            "pid": 50709,
            "port": 9443,
            "protocol": "tcp",
            "stime": "Tue May 25 15:30:13 2021",
            "user": "tomcat"
        }
    )
    params_set_one_sw[1].append(
        {
            "bindings": [{"address": "::",
                          "class": "service",
                          "port": 9443,
                          "protocol": "tcp"}],
            "type": "Apache Tomcat Servlet Engine",
            "discovery_time": "2022-05-26T18:00:00+02:00",
            "process": {
                "children": [
                    {
                        "children": [],
                        "cmdline": "/usr/local/openjdk-17/bin/java "
                                   "-Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties"
                                   " -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager"
                                   " -Xmx7876m -Xms3846m"
                                   " -Djdk.tls.ephemeralDHKeySize=2048"
                                   " -Djava.protocol.handler.pkgs=org.apache.catalina.webresources"
                                   " -Dorg.apache.catalina.security.SecurityListener.UMASK=0027"
                                   " -Xlog:gc=debug:file=logs/gc.log:time,uptime,level,tags:filecount=10,filesize=100m"
                                   " -javaagent:/usr/local/tomcat/lib/elastic-apm-agent-1.28.1.jar"
                                   " -Delastic.apm.service_name=cmdb"
                                   " -Delastic.apm.server_url=http://192.168.8.53:8200 -Delastic.apm.environment=dev"
                                   " -Delastic.apm.enabled=true -Delastic.apm.profiling_inferred_spans_enabled=true"
                                   " -Delastic.apm.profiling_inferred_spans_min_duration=250ms"
                                   " -Delastic.apm.profiling_inferred_spans_included_classes=org.cmdbuild.*"
                                   " -Dignore.endorsed.dirs="
                                   " -classpath /usr/local/tomcat/bin/bootstrap.jar"
                                   ":/usr/local/tomcat/bin/tomcat-juli.jar"
                                   " -Dcatalina.base=/usr/local/tomcat -Dcatalina.home=/usr/local/tomcat"
                                   " -Djava.io.tmpdir=/usr/local/tomcat/temp"
                                   " org.apache.catalina.startup.Bootstrap start",
                        "cwd": "/usr/local/openjdk-17/bin/",
                        "pid": "50748",
                        "ppid": "50709",
                        "user": "root"
                    }],
                "cmdline": "/bin/sh -c /usr/local/bin/docker-entrypoint.sh catalina.sh run",
                "cwd": "/bin/",
                "pid": "50709",
                "ppid": "50689",
                "user": "root",
                'listening_ports': [9443]
            },
            "listening_ports": [9443]
        }
    )
    return params_set_one_sw


@pytest.mark.parametrize(argnames=['params_and_expected_result'],
                         argvalues=[
                             (lazy_fixture('params_set_one_sw'),),
                             (lazy_fixture('params_set_two_sw'),),
                             (lazy_fixture('params_set_no_sw'),)]
                         )
def test_get_software_ok(normalize, params_and_expected_result):
    params, expected_result = params_and_expected_result
    result = ActionModule(*[None] * 6).process_software(**params)
    assert normalize(result) == normalize(expected_result)
