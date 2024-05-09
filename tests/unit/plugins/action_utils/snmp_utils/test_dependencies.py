from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible_collections.datadope.discovery.plugins.action_utils.snmp_utils.utils import index_dependency


@pytest.fixture
def params_index_dependency():
    params = {
        "config_dependencies": [
            {
                "dest_table": "interfaces",
                "dependencies": [
                    {
                        "table": "if_mib",
                        "index": {
                            "type": "index"
                        }
                    }
                ]
            },
            {
                "dest_table": "ips",
                "dependencies": [
                    {
                        "table": "interfaces",
                        "index": {
                            "type": "value",
                            "name": "ipAdEntIfIndex"
                        }
                    }
                ]
            }
        ],
        "tagged_result": {
            "if_mib": {
                "1": {
                    "_index": "1",
                    "ifAlias": "TO-ZhuanWanghuiju-10.3.0.44",
                    "ifHighSpeed": "1000"
                },
                "134217728": {
                    "_index": "134217728",
                    "ifAlias": "SWITCH IP INTERFACE",
                    "ifHighSpeed": "0"
                },
                "16385": {
                    "_index": "16385",
                    "ifAlias": "802.1Q VLAN",
                    "ifHighSpeed": "0"
                },
                "16389": {
                    "_index": "16389",
                    "ifAlias": "802.1Q VLAN",
                    "ifHighSpeed": "0"
                }
            },
            "interfaces": {
                "1": {
                    "ifType": "6",
                    "_index": "1",
                    "ifAdminStatus": "up",
                    "ifAlias": "TO-ZhuanWanghuiju-10.3.0.44",
                    "ifDescr": "TO-ZhuanWanghuiju-10.3.0.44",
                    "ifHighSpeed": "1000",
                    "ifIndex": "1",
                    "ifMtu": "1500",
                    "ifOperStatus": "up",
                    "ifPhysAddress": "001a1e0321e1",
                    "ifSpeed": "1000000000"
                },
                "134217728": {
                    "_index": "134217728",
                    "ifAdminStatus": "up",
                    "ifIndex": "134217728",
                    "ifOperStatus": "up",
                    "ifPhysAddress": "001a1e0321e0",
                    "ifSpeed": "0"
                },
                "16385": {
                    "_index": "16385",
                    "ifAdminStatus": "up",
                    "ifIndex": "16385",
                    "ifOperStatus": "up",
                    "ifPhysAddress": "001a1e0321e0",
                    "ifSpeed": "0"
                },
                "16389": {
                    "_index": "16389",
                    "ifAdminStatus": "up",
                    "ifIndex": "16389",
                    "ifOperStatus": "up",
                    "ifPhysAddress": "001a1e0321e0",
                    "ifSpeed": "0"
                }
            },
            "ips": {
                "10.0.18.2": {
                    "_index": "10.0.18.2",
                    "ipAdEntAddr": "10.0.18.2",
                    "ipAdEntIfIndex": "16385",
                    "ipAdEntNetMask": "255.255.255.252"
                },
                "10.8.0.1": {
                    "_index": "10.8.0.1",
                    "ipAdEntAddr": "10.8.0.1",
                    "ipAdEntIfIndex": "134217728",
                    "ipAdEntNetMask": "255.255.255.255"
                },
                "114.255.40.100": {
                    "_index": "114.255.40.100",
                    "ipAdEntAddr": "114.255.40.100",
                    "ipAdEntIfIndex": "16389",
                    "ipAdEntNetMask": "255.255.255.192"
                }
            }
        }
    }

    expected_result = {
        "if_mib": {
            "1": {
                "_index": "1",
                "ifAlias": "TO-ZhuanWanghuiju-10.3.0.44",
                "ifHighSpeed": "1000"
            },
            "134217728": {
                "_index": "134217728",
                "ifAlias": "SWITCH IP INTERFACE",
                "ifHighSpeed": "0"
            },
            "16385": {
                "_index": "16385",
                "ifAlias": "802.1Q VLAN",
                "ifHighSpeed": "0"
            },
            "16389": {
                "_index": "16389",
                "ifAlias": "802.1Q VLAN",
                "ifHighSpeed": "0"
            }
        },
        "interfaces": {
            "1": {
                "ifType": "6",
                "_index": "1",
                "ifAdminStatus": "up",
                "ifAlias": "TO-ZhuanWanghuiju-10.3.0.44",
                "ifDescr": "TO-ZhuanWanghuiju-10.3.0.44",
                "ifHighSpeed": "1000",
                "ifIndex": "1",
                "ifMtu": "1500",
                "ifOperStatus": "up",
                "ifPhysAddress": "001a1e0321e1",
                "ifSpeed": "1000000000"
            },
            "134217728": {
                "_index": "134217728",
                "ifAdminStatus": "up",
                "ifIndex": "134217728",
                "ifOperStatus": "up",
                "ifPhysAddress": "001a1e0321e0",
                "ifSpeed": "0",
                "ifAlias": "SWITCH IP INTERFACE",
                "ifHighSpeed": "0"
            },
            "16385": {
                "_index": "16385",
                "ifAdminStatus": "up",
                "ifIndex": "16385",
                "ifOperStatus": "up",
                "ifPhysAddress": "001a1e0321e0",
                "ifSpeed": "0",
                "ifAlias": "802.1Q VLAN",
                "ifHighSpeed": "0"
            },
            "16389": {
                "_index": "16389",
                "ifAdminStatus": "up",
                "ifIndex": "16389",
                "ifOperStatus": "up",
                "ifPhysAddress": "001a1e0321e0",
                "ifSpeed": "0",
                "ifAlias": "802.1Q VLAN",
                "ifHighSpeed": "0"
            }
        },
        "ips": {
            "10.0.18.2": {
                "_index": "10.0.18.2",
                "ipAdEntAddr": "10.0.18.2",
                "ipAdEntIfIndex": "16385",
                "ipAdEntNetMask": "255.255.255.252",
                "ifAdminStatus": "up",
                "ifIndex": "16385",
                "ifOperStatus": "up",
                "ifPhysAddress": "001a1e0321e0",
                "ifSpeed": "0",
                "ifAlias": "802.1Q VLAN",
                "ifHighSpeed": "0"
            },
            "10.8.0.1": {
                "_index": "10.8.0.1",
                "ipAdEntAddr": "10.8.0.1",
                "ipAdEntIfIndex": "134217728",
                "ipAdEntNetMask": "255.255.255.255",
                "ifAdminStatus": "up",
                "ifIndex": "134217728",
                "ifOperStatus": "up",
                "ifPhysAddress": "001a1e0321e0",
                "ifSpeed": "0",
                "ifAlias": "SWITCH IP INTERFACE",
                "ifHighSpeed": "0"
            },
            "114.255.40.100": {
                "_index": "114.255.40.100",
                "ipAdEntAddr": "114.255.40.100",
                "ipAdEntIfIndex": "16389",
                "ipAdEntNetMask": "255.255.255.192",
                "ifAdminStatus": "up",
                "ifIndex": "16389",
                "ifOperStatus": "up",
                "ifPhysAddress": "001a1e0321e0",
                "ifSpeed": "0",
                "ifAlias": "802.1Q VLAN",
                "ifHighSpeed": "0"
            }
        }
    }
    return params, expected_result


@pytest.mark.parametrize(argnames=['params_and_expected_result'],
                         argvalues=[
                             ('params_index_dependency',)]
                         )
def test_dependencies(params_and_expected_result, request):
    params_and_expected_result = request.getfixturevalue(params_and_expected_result)
    params, expected_result = params_and_expected_result
    tagged_result = params['tagged_result']
    for config in params['config_dependencies']:
        for dependency in config['dependencies']:
            index_dependency(dependency, config['dest_table'], tagged_result)

    assert tagged_result == expected_result
