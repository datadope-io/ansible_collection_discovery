from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from pytest_lazyfixture import lazy_fixture

from ansible_collections.datadope.discovery.plugins.action_utils.snmp_utils.utils import processed_templating_result


@pytest.fixture
def params_processed_template():
    params = {

        "snmp_template": {
            "generic_template": {
                "if_mib": {
                    "entries": {
                        "ifAlias": {
                            "oid": ".18"
                        },
                        "ifHighSpeed": {
                            "oid": ".15"
                        }
                    },
                    "oid": "1.3.6.1.2.1.31.1.1.1",
                    "omit": True,
                    "type": "list"
                },
                "interfaces": {
                    "dependencies": [
                        {
                            "index": {
                                "type": "index"
                            },
                            "table": "if_mib"
                        }
                    ],
                    "entries": {
                        "ifType": {
                            "oid": ".3"
                        },
                        "ifAdminStatus": {
                            "oid": ".7",
                            "post_process": "lookup_adminstatus"
                        },
                        "ifDescr": {
                            "oid": ".2"
                        },
                        "ifIndex": {
                            "oid": ".1",
                            "omit": True
                        },
                        "ifMtu": {
                            "oid": ".4"
                        },
                        "ifOperStatus": {
                            "oid": ".8",
                            "post_process": "lookup_operstatus"
                        },
                        "ifPhysAddress": {
                            "oid": ".6",
                            "post_process": "decode_mac"
                        },
                        "ifSpeed": {
                            "oid": ".5"
                        }
                    },
                    "oid": "1.3.6.1.2.1.2.2.1",
                    "omit": True,
                    "type": "list"
                },
                "ips": {
                    "dependencies": [
                        {
                            "index": {
                                "name": "ipAdEntIfIndex",
                                "type": "value"
                            },
                            "table": "interfaces"
                        }
                    ],
                    "entries": {
                        "ipAdEntAddr": {
                            "oid": ".1"
                        },
                        "ipAdEntIfIndex": {
                            "oid": ".2",
                            "omit": True
                        },
                        "ipAdEntNetMask": {
                            "oid": ".3"
                        }
                    },
                    "oid": "1.3.6.1.2.1.4.20.1",
                    "type": "list"
                },
                "sysContact": {
                    "oid": "1.3.6.1.2.1.1.4.0"
                },
                "sysDescr": {
                    "oid": "1.3.6.1.2.1.1.1.0",
                    "post_process": "decode_hex"
                },
                "sysLocation": {
                    "oid": "1.3.6.1.2.1.1.6.0"
                },
                "sysName": {
                    "oid": "1.3.6.1.2.1.1.5.0"
                },
                "sysObjectId": {
                    "oid": "1.3.6.1.2.1.1.2.0"
                },
                "sysUpTime": {
                    "oid": "1.3.6.1.2.1.1.3.0"
                }
            }
        },
        "snmp_facts": {
            "_indexed_result": {
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
                        "ifAdminStatus": "1",
                        "ifDescr": "TO-ZhuanWanghuiju-10.3.0.44",
                        "ifIndex": "1",
                        "ifMtu": "1500",
                        "ifOperStatus": "1",
                        "ifPhysAddress": "0x001a1e0321e1",
                        "ifSpeed": "1000000000"
                    },
                    "134217728": {
                        "ifType": "24",
                        "_index": "134217728",
                        "ifAdminStatus": "1",
                        "ifDescr": "SWITCH IP INTERFACE",
                        "ifIndex": "134217728",
                        "ifMtu": "1500",
                        "ifOperStatus": "1",
                        "ifPhysAddress": "0x001a1e0321e0",
                        "ifSpeed": "0"
                    },
                    "16385": {
                        "ifType": "136",
                        "_index": "16385",
                        "ifAdminStatus": "1",
                        "ifDescr": "802.1Q VLAN",
                        "ifIndex": "16385",
                        "ifMtu": "1500",
                        "ifOperStatus": "1",
                        "ifPhysAddress": "0x001a1e0321e0",
                        "ifSpeed": "0"
                    },
                    "16389": {
                        "ifType": "136",
                        "_index": "16389",
                        "ifAdminStatus": "1",
                        "ifDescr": "802.1Q VLAN",
                        "ifIndex": "16389",
                        "ifMtu": "1500",
                        "ifOperStatus": "1",
                        "ifPhysAddress": "0x001a1e0321e0",
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
            },
            "sysContact": "",
            "sysDescr": "ArubaOS (MODEL: Aruba7210), Version 6.5.1.6 (60228)",
            "sysLocation": "",
            "sysName": "DUMSYS-03",
            "sysObjectId": "1.3.6.1.4.1.14823.1.1.32",
            "sysUpTime": "2319388"
        }
    }

    expected_result = {
        "sysContact": "",
        "sysDescr": "ArubaOS (MODEL: Aruba7210), Version 6.5.1.6 (60228)",
        "sysLocation": "",
        "sysName": "DUMSYS-03",
        "sysObjectId": "1.3.6.1.4.1.14823.1.1.32",
        "sysUpTime": "2319388",
        "ips": [
            {
                "ipAdEntAddr": "10.0.18.2",
                "ipAdEntNetMask": "255.255.255.252",
                "ifType": "136",
                "ifAdminStatus": "up",
                "ifDescr": "802.1Q VLAN",
                "ifMtu": "1500",
                "ifOperStatus": "up",
                "ifPhysAddress": "001a1e0321e0",
                "ifSpeed": "0",
                "ifAlias": "802.1Q VLAN",
                "ifHighSpeed": "0"
            },
            {
                "ipAdEntAddr": "10.8.0.1",
                "ipAdEntNetMask": "255.255.255.255",
                "ifType": "24",
                "ifAdminStatus": "up",
                "ifDescr": "SWITCH IP INTERFACE",
                "ifMtu": "1500",
                "ifOperStatus": "up",
                "ifPhysAddress": "001a1e0321e0",
                "ifSpeed": "0",
                "ifAlias": "SWITCH IP INTERFACE",
                "ifHighSpeed": "0"
            },
            {
                "ipAdEntAddr": "114.255.40.100",
                "ipAdEntNetMask": "255.255.255.192",
                "ifType": "136",
                "ifAdminStatus": "up",
                "ifDescr": "802.1Q VLAN",
                "ifMtu": "1500",
                "ifOperStatus": "up",
                "ifPhysAddress": "001a1e0321e0",
                "ifSpeed": "0",
                "ifAlias": "802.1Q VLAN",
                "ifHighSpeed": "0"
            }
        ]
    }
    return params, expected_result


@pytest.mark.parametrize(argnames=['params_and_expected_result'],
                         argvalues=[
                             (lazy_fixture('params_processed_template'),)]
                         )
def test_util_process_templating(params_and_expected_result):
    params, expected_result = params_and_expected_result
    result = processed_templating_result(
        snmp_template=params['snmp_template'],
        snmp_facts=params['snmp_facts']
    )

    assert result == expected_result
