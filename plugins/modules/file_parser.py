#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: file_parser

short_description: Processes the given file with the specified parser.

version_added: "1.0.0"

description: Processes the given file using one of the supported parsers, supporting the injection of env vars.

options:
  file_path:
    description: Path of the file to parse.
    required: true
    type: str
  parser:
    description: Parser that will handle the parsing of the file.
    required: true
    type: str
    choices:
      - apache_webserver
      - haproxy
      - keepalived
      - nginx
  env_vars:
    description: Environment variables that will be injected into the parser.
    required: false
    type: dict
  path_prefix:
    description: Prefix that will be appended to every path that the parser will access during its operation.
    required: false
    type: str
  strict_vars:
    description: Determines if the process should fail if a defined environment variable is not available.
    required: false
    type: bool
    default: false

author:
  - Datadope (@datadope)
'''

EXAMPLES = r'''
# List running processes
- name: Parse config file
  file_parser:
    file_path: "/etc/httpd/conf/httpd.conf"
    parser: "apache_webserver"
'''

RETURN = r'''
parsed:
  description: Parsed file.
  returned: always
  type: dict
'''

import os  # noqa
import pwd  # noqa
import re  # noqa
import sys  # noqa

from ansible.module_utils.basic import AnsibleModule  # noqa


def get_parser_loader_func(parser):
    # We have to follow this approach because ansible packaging does not support dynamic imports
    # with the AnsiballZ system, since it requires the module_utils to be explicitly imported.

    loader_func = None

    if parser == 'apache_webserver':
        from ansible_collections.datadope.discovery.plugins.module_utils.file_parser.apache_webserver.loader \
            import make_loader
        loader_func = make_loader
    elif parser == 'haproxy':
        from ansible_collections.datadope.discovery.plugins.module_utils.file_parser.haproxy.loader \
            import make_loader
        loader_func = make_loader
    elif parser == 'keepalived':
        from ansible_collections.datadope.discovery.plugins.module_utils.file_parser.keepalived.loader \
            import make_loader
        loader_func = make_loader
    elif parser == 'nginx':
        from ansible_collections.datadope.discovery.plugins.module_utils.file_parser.nginx.loader \
            import make_loader
        loader_func = make_loader

    return loader_func


def parse_file(module):
    file_path = module.params['file_path']
    parser = module.params['parser']
    env_vars = module.params['env_vars']
    path_prefix = module.params['path_prefix']
    strict_vars = module.params['strict_vars']

    parsed = None
    try:
        loader_func = get_parser_loader_func(parser)
        parser_loader = loader_func(file_path, envvars=env_vars, pathprefix=path_prefix, strictvars=strict_vars)
        parsed = parser_loader.load(file_path)
    except Exception as e:
        module.fail_json(msg="Could not parse file '{0}' with parser '{1}': {2}".format(file_path, parser, e))

    return parsed


argument_spec = dict(
    file_path=dict(type='str', required=True),
    parser=dict(type='str', required=True, choices=[
        'apache_webserver',
        'haproxy',
        'keepalived',
        'nginx'
    ]),
    env_vars=dict(type='dict', required=False, default={}),
    path_prefix=dict(type='str', required=False, default=''),
    strict_vars=dict(type='bool', required=False, default=False)
)


def setup_module_object():
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    return module


def validate_parameters(parameters):  # noqa
    pass


def main():
    result = dict(
        changed=False,
        parsed_file=None
    )
    module = setup_module_object()
    validate_parameters(module.params)
    # Make main process method independent of ansible objects to facilitate tests (if possible)
    parsed = parse_file(module=module)
    if parsed is not None:
        result['parsed'] = parsed
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()
