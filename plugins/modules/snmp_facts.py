#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: snmp_facts
author:
- Datadope (@datadope-io)
short_description: Retrieve facts for a device using SNMP
description:
    - Retrieve facts for a device using SNMP, the facts will be
      inserted to the ansible_facts key.
requirements:
    - pysnmp
options:
    host:
        description:
            - Set to target SNMP server (normally C({{ inventory_hostname }})).
        type: str
        required: true
    port:
        description:
            - SNMP UDP port number.
        type: int
        default: 161
    timeout:
        description:
            - Response timeout in seconds.
        type: int
        default: 10
    retries:
        description:
            - Maximum number of request retries, 1 retries means just a single request.
        type: int
        default: 1
    version:
        description:
            - SNMP Version to use, C(v2), C(v2c) or C(v3).
        type: str
        required: true
        choices: ['v2c', 'v2', '2c', '2', 'v3', '3']
    community:
        description:
            - The SNMP community string, required if I(version) is C(v2c).
        type: str
    security_level:
        description:
            - Authentication level.
            - Required if I(version) is C(v3).
        type: str
        choices: [ noAuthnoPriv, authNoPriv, authPriv ]
    username:
        description:
            - Username for SNMPv3.
            - Required if I(version) is C(v3).
        type: str
    integrity:
        description:
            - Hashing algorithm.
            - Required if I(version) is C(v3).
        type: str
        choices: [ md5, sha ]
    authkey:
        description:
            - Authentication key.
            - Required I(version) is C(v3).
        type: str
    privacy:
        description:
            - Encryption algorithm.
            - Required if I(level) is C(authPriv).
        type: str
        choices: [ aes, des ]
    privkey:
        description:
            - Encryption key.
            - Required if I(level) is C(authPriv).
        type: str
    context_name:
        description:
            - Specifies an SNMP context by its name, a case-sensitive string of 1 to 32 characters.
        type: str
    context_engine_id:
        description:
            - Unique SNMP Engine ID for the administrative domain.
        type: str
    sysobject_ids:
        description:
            - Dictionary of template definitions by brand, model and device type for discovered sysObjectId.
            - If not defined, brand, model and device type will not be discovered.
            - Requires template_content if not defined.
        type: dict
        default: {}
    templates_path:
        description:
            - Path where template files are located.
        type: str
'''

EXAMPLES = r'''
- name: Gather facts with SNMP version 2
  datadope.discovery.snmp_facts:
    host: '{{ inventory_hostname }}'
    version: v2c
    community: public
    sysobject_ids: "{{ sysobject_ids }}"
    templates_path: "{{ snmp_discovery__templates_directory_path }}"
- name: Gather facts using SNMP version 3
  datadope.discovery.snmp_facts:
    host: '{{ inventory_hostname }}'
    version: v3
    security_level: authPriv
    username: username
    integrity: md5
    authkey: abc12345
    privacy: aes
    privkey: def6789
    context_name: example-abc
    context_engine_id: 01234xyz
    sysobject_ids: '{{ sysobject_ids }}'
    templates_path: '{{ snmp_discovery__templates_directory_path }}'
'''

RETURN = r'''
ansible_facts:
  description: Facts to add to ansible_facts.
  returned: always
  type: dict
  sample: {
    "snmp": {
        "brand": "Aruba",
        "ips": [
            {
                "IfType": "136",
                "ifAdminStatus": "up",
                "ifDescr": "802.1Q VLAN",
                "ifMtu": "1500",
                "ifOperStatus": "up",
                "ifPhysAddress": "001a1e0321e0",
                "ipAdEntAddr": "192.168.1.25",
                "ipAdEntNetMask": "255.255.255.252"
            },
        ],
        "model": "7210 Controller",
        "snmp_type": "NETWORKING",
        "sysDescr": "ArubaOS (MODEL: Aruba7210), Version 6.5.1.6 (60228)",
        "sysName": "DUMSYS-01",
        "sysObjectId": "1.3.6.1.4.1.14823.1.1.32",
        "sysUpTime": "10054113"
    }
  }
'''

import traceback

PYSNMP_IMP_ERR = None
try:
    from pysnmp.entity.rfc3413.oneliner import cmdgen
    from pysnmp.proto.rfc1905 import EndOfMibView
    from pysnmp.proto import rfc1902

    HAS_PYSNMP = True
except Exception:
    PYSNMP_IMP_ERR = traceback.format_exc()
    HAS_PYSNMP = False

from ansible.module_utils.basic import AnsibleModule, missing_required_lib


def get_connection_params(module):
    # SNMP connection params
    host = module.params.get('host')
    port = module.params.get('port')
    timeout = module.params.get('timeout')
    retries = module.params.get('retries')

    connection_params = {
        'snmp_auth': get_snmp_auth(module=module),
        'udp_transport_target': cmdgen.UdpTransportTarget((host, port), timeout=timeout, retries=retries),
    }
    if module.params['version'] in ("v3", "3") and ("context_engine_id", "context_name") in module.params:
        connection_params.update({'snmp_context': {
            'contextName': module.params.get('context_name'),
            'contextEngineId': rfc1902.OctetString(hexValue=module.params['context_engine_id']) if module.params.get(
                'context_engine_id') else None
        }})

    return connection_params


def get_snmp_auth(module):
    if module.params['version'] in ("v2c", "v2", "2c", "2"):
        if module.params.get('community') is not None:
            return cmdgen.CommunityData(module.params['community'])
        else:
            module.fail_json(msg='Community not set when using snmp version 2')

    elif module.params['version'] in ("v3", "3"):
        if module.params.get('username') is None:
            module.fail_json(msg='Username not set when using snmp version 3')

        if module.params.get('security_level').lower() is None:
            module.fail_json(msg='Security level not set when using snmp version 3')

        if module.params.get('security_level').lower() == "noauthnopriv":
            return cmdgen.UsmUserData(userName=module.params['username'])

        if module.params.get('security_level').lower() == "authpriv" and module.params.get('privacy') is None:
            module.fail_json(msg='Privacy algorithm not set when using authPriv')

        v3_params = {
            'authKey': module.params.get('authkey'),
            'privKey': module.params.get('privkey')
        }

        if module.params.get('privacy').lower() == "aes":
            v3_params['privProtocol'] = cmdgen.usmAesCfb128Protocol
        elif module.params.get('privacy').lower() == "des":
            v3_params['privProtocol'] = cmdgen.usmDESPrivProtocol

        if module.params.get('integrity').lower() == "sha":
            v3_params['authProtocol'] = cmdgen.usmHMACSHAAuthProtocol
        elif module.params.get('integrity').lower() == "md5":
            v3_params['authProtocol'] = cmdgen.usmHMACMD5AuthProtocol

        return cmdgen.UsmUserData(userName=module.params['username'], **v3_params)

    return None


def generate_oids_to_consult(entries, base_oid=''):
    return [cmdgen.MibVariable(
        ".{0}".format(entry['oid']) if not entry.get('oid', '').startswith('.') else
        ".{0}{1}".format(base_oid, entry['oid']), ) for entry in entries.values()]


def snmp_pre_process(module):
    default_oids = {
        'sysDescr': {
            'oid': '1.3.6.1.2.1.1.1.0',
            'post_process': 'decode_hex'
        },
        'sysObjectId': {
            'oid': '1.3.6.1.2.1.1.2.0'
        }
    }

    connection_params = get_connection_params(module=module)

    return get_scalar_snmp_facts(
        module,
        connection_params,
        default_oids
    )


def get_snmp_facts_by_template(module):
    result = {}
    connection_params = get_connection_params(module=module)
    for val in module.params.get('_template_content', {}).values():
        for key, config in val.items():
            if 'type' in config.keys():
                if config['type'] == 'list':
                    table_oids = generate_oids_to_consult(config['entries'], config['oid'])
                    snmp_result = exec_cmd_command(module, connection_params, table_oids, True)
                    for var_binds in snmp_result:
                        process_result = process_snmp_result(var_binds, config['entries'], config['oid'], True)
                        result.setdefault('_indexed_result', {}).setdefault(key, {}).update(process_result.items())
            else:
                result.setdefault('_scalar_entries', {})[key] = config

    result.update(get_scalar_snmp_facts(module, connection_params, result.pop('_scalar_entries', None)))

    return result


def get_scalar_snmp_facts(module, connection_params, scalar_entries):
    if scalar_entries:
        return process_snmp_result(
            exec_cmd_command(
                module,
                connection_params,
                generate_oids_to_consult(scalar_entries)),
            scalar_entries)

    return {}


def process_snmp_result(result, entries, base_oid='', table=False):
    processed_result = {}
    for oid, val in result:
        if isinstance(val, EndOfMibView):
            continue
        current_oid = oid.prettyPrint()
        current_val = val.prettyPrint()
        for attr, cfg in entries.items():
            config_oid = cfg.get('oid') if not cfg.get('oid', '').startswith(".") \
                else ''.join([base_oid, cfg.get('oid')])
            if table and config_oid in current_oid:
                index_tag = current_oid.replace("{0}.".format(config_oid), '')
                processed_result.setdefault(index_tag, {'_index': index_tag})[attr] = current_val
            elif config_oid == current_oid:
                processed_result[attr] = current_val

    return processed_result


def exec_cmd_command(module, connection_params, oids_to_consult, table=False):
    if not table:
        command = cmdgen.CommandGenerator().getCmd
    else:
        command = cmdgen.CommandGenerator().nextCmd

    error_indication, error_status, error_index, result = command(
        connection_params['snmp_auth'],
        connection_params['udp_transport_target'],
        lookupMib=False,
        *oids_to_consult,
        **connection_params.get('snmp_context', {})
    )

    if error_indication:
        module.fail_json(msg=str(error_indication))

    if error_status:
        module.fail_json(msg=str(
            '%s at %s' %
            (error_status.prettyPrint(),
             error_index and result[0][int(error_index) - 1] or '?')))

    return result


def setup_module_object():
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type='str', required=True),
            port=dict(type='int', required=False, default=161),
            timeout=dict(type='int', required=False, default=10),
            retries=dict(type='int', required=False, default=1),
            version=dict(type='str', required=True, choices=['v2c', 'v2', '2c', '2', 'v3', '3']),
            community=dict(type='str', required=False, no_log=True),
            security_level=dict(type='str', choices=['noAuthnoPriv', 'authNoPriv', 'authPriv']),
            username=dict(type='str', required=False),
            integrity=dict(type='str', choices=['md5', 'sha']),
            authkey=dict(type='str', required=False, no_log=True),
            privacy=dict(type='str', required=False, choices=['aes', 'des']),
            privkey=dict(type='str', required=False, no_log=True),
            context_engine_id=dict(type='str', required=False, default=None),
            context_name=dict(type='str', required=False, default=None),
            sysobject_ids=dict(type='dict', required=False, default={}),
            templates_path=dict(type='str', required=False),
            _template_content=dict(type='dict', required=False),
            _enterprise_numbers=dict(type='dict', required=False),
            _pre_check=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )
    return module


def validate_parameters(parameters):  # noqa
    pass


def main():
    result = dict(
        changed=False,
        ansible_facts=dict()
    )

    module = setup_module_object()
    if not HAS_PYSNMP:
        module.fail_json(msg=missing_required_lib('pysnmp'), exception=PYSNMP_IMP_ERR)
    validate_parameters(module.params)
    # Make main process method independent of ansible objects to facilitate tests (if possible)
    snmp_info = snmp_pre_process(module=module) if not module.params.get('_pre_check') \
        else get_snmp_facts_by_template(module=module)

    if snmp_info is not None:
        result['ansible_facts'] = {"snmp": snmp_info}
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()
