#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: check_connection

short_description: Checks if a given endpoint is up and, if so, if it has tls enabled .

version_added: "1.0.0"

description: Checks if a given endpoint (address + port) is up trying to connect to it  and, if so, checks
  if it has tls enabled by trying to cause a certificate error while connecting.

options:
  address:
    description:
      - The ip we are trying to connect to.
    type: str
    required: true
  port:
    description:
      - The port of the address.
    type: int
    required: true
  timeout:
    description:
      - The time in seconds that the process is going to be waiting for the checking to take place. If this checking
       takes more than the specified timeout, this will result in an error message
    type: int
    required: false
    default: 1


author:
    - Datadope (@datadope)
'''

EXAMPLES = r'''
# Check if ports has tls enabled
- name: Check http or https
  run_module:
    check_connection:
      address: "127.0.0.1"
      port: 38956
'''

RETURN = r'''
available:
  description: If the given endpoint is available
  returned: always
  type: bool
identified_as:
  description: If the given endpoint has tls enabled or not
  returned: always
  type: bool
'''

import socket  # noqa
import ansible.module_utils.six.moves.urllib.error  # noqa
import ansible.module_utils.six.moves.urllib.parse  # noqa
import ansible.module_utils.six.moves.urllib.request  # noqa

from ansible.module_utils.basic import AnsibleModule  # noqa

argument_spec = dict(
    address=dict(type='str', required=True),
    port=dict(type='int', required=True),
    timeout=dict(type='int', required=False, default=1)
)


def check_port_open(address, port, timeout):
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        _socket.connect((address, int(port)))
        _socket.settimeout(timeout)
        _socket.shutdown(2)
        return True
    except Exception:
        return False


def check_http_or_https(address, port, timeout):
    """Returns 'http' if endpoint is http, 'https' if endpoint is https, or None if it can't be identified

    Endpoint must be addressed according to the following pattern: ip:port or host:port
    """
    _endpoint = address + ':' + str(port)
    try:
        ansible.module_utils.six.moves.urllib.request.urlopen('https://' + _endpoint, timeout)
        return "https"
    except ansible.module_utils.six.moves.urllib.error.HTTPError:
        return "https"
    except ansible.module_utils.six.moves.urllib.error.URLError:
        try:
            ansible.module_utils.six.moves.urllib.request.urlopen('http://' + _endpoint, timeout)
            return "http"
        except ansible.module_utils.six.moves.urllib.error.HTTPError:
            return "http"
        except Exception:
            pass
    except Exception:
        pass

    return None


def check_connection(module):
    check_mode = module.check_mode
    if check_mode:
        return None, None

    address = module.params['address']
    port = module.params['port']
    timeout = module.params['timeout']

    is_port_open = check_port_open(address, port, timeout)
    identified_as = None
    if is_port_open is True:
        identified_as = check_http_or_https(address, port, timeout)

    return is_port_open, identified_as


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
        available=False,
        identified_as=False or None
    )
    module = setup_module_object()
    validate_parameters(module.params)
    # Make main process method independent of ansible objects to facilitate tests (if possible)
    available, identified_as = check_connection(module=module)
    result['available'] = available
    result['identified_as'] = identified_as

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()
