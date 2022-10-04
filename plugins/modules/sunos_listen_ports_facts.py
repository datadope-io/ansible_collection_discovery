#!/usr/bin/python

# Copyright: (c) 2022, Datadope, S.L. <info@datadope.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: sunos_listen_ports_facts

short_description: Gathers the facts of the listening ports of the SunOS machine

version_added: "1.0.0"

description: Gathers the information of the TCP and UDP ports of the machine and the related processes.

options: {}

author:
    - Datadope (@datadope)
'''

EXAMPLES = r'''
# Gather ports facts
- name: Gather ports facts
  datadope.discovery.sunos_listen_ports_facts: {}
'''

RETURN = r'''
tcp_listen:
    description: List of dicts with the detected TCP ports
    returned: success
    type: list
    elements: dict
    sample: [
        {
            "address": "127.0.0.1",
            "name": "python",
            "pid": 816,
            "port": 150,
            "protocol": "tcp",
            "stime": "Thu Nov 15 12:25:29  2018",
            "user": "root"
        }
    ]
udp_listen:
    description: List of dicts with the detected UDP ports
    returned: success
    type: list
    elements: dict
    sample: [
        {
            "address": "127.0.0.1",
            "name": "python",
            "pid": 816,
            "port": 151,
            "protocol": "udp",
            "stime": "Thu Nov 15 12:25:29  2018",
            "user": "root"
        }
    ]
'''

import os  # noqa
import re  # noqa
import sys  # noqa

from datetime import datetime  # noqa

from ansible.module_utils.basic import AnsibleModule  # noqa
from ansible.module_utils.six import iteritems  # noqa


def _get_pid_stime(pid):
    stime = ''

    try:
        timestamp = os.stat('/proc/%s' % pid).st_ctime
        stime = datetime.fromtimestamp(int(timestamp)).strftime('%C')
    except OSError:
        pass

    return stime


def _run_command(module, command):
    rc, stdout, stderr = module.run_command(args=command,
                                            use_unsafe_shell=True)

    return rc, stdout, stderr


def build_pid_index(module):
    rc, stdout, stderr = _run_command(module=module,
                                      command='ps -e -o pid= -o fname= -o user=')
    pid_index = {}
    if rc == 0 and stdout:
        for line in stdout.splitlines():
            process = re.findall(r'([\d-]+)\s+(.*?)\s+(.*)', line.strip(), re.DOTALL)
            if process:
                pid, name, user = process[0]
                pid_index[pid] = {'pid': pid, 'name': name, 'user': user}

    return pid_index


def build_listen_ports(module):
    tcp_listen = []
    udp_listen = []

    added_ports = []
    pid_index = build_pid_index(module)

    pids = os.listdir('/proc')
    for pid in pids:
        path = '/proc/' + pid

        if not os.path.isdir(path):
            continue

        rc, stdout, stderr = _run_command(module=module,
                                          command='pfiles %s 2>/dev/null' % path)

        if rc != 0 or not stdout:
            continue

        protocol = None
        for line in stdout.splitlines():

            if 'SOCK_STREAM' in line:
                protocol = 'tcp'
                continue

            elif 'SOCK_DGRAM' in line:
                protocol = 'udp'
                continue

            elif 'AF_INET' in line:
                listener = line.split()

                if len(listener) != 5:
                    continue

                if listener[0].strip(':') == 'peername':
                    continue

                address = listener[2]
                port = listener[4]

                listener_id = '%s:%s:%s' % (address, port, protocol)

                if listener_id in added_ports:
                    continue

                port_data = {
                    'address': address,
                    'port': int(port),
                    'protocol': protocol,
                    'stime': _get_pid_stime(pid=pid)
                }

                port_data.update(pid_index.get(pid, {}))

                if protocol == 'tcp':
                    tcp_listen.append(port_data)
                elif protocol == 'udp':
                    udp_listen.append(port_data)
                added_ports.append(listener_id)

    return tcp_listen, udp_listen


argument_spec = dict()


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


def get_listening_ports(module):
    check_mode = module.check_mode
    if check_mode:
        return None
    platform = sys.platform

    if 'sunos' not in platform:
        module.fail_json(msg='This module requires Linux.')

    return build_listen_ports(module)


def main():
    result = dict(
        changed=False,
        ansible_facts=dict()
    )
    module = setup_module_object()
    validate_parameters(module.params)
    # Make main process method independent of ansible objects to facilitate tests (if possible)
    tcp_listen, udp_listen = get_listening_ports(module=module)
    if tcp_listen is not None and udp_listen is not None:
        result['ansible_facts'] = {
            'tcp_listen': tcp_listen,
            'udp_listen': udp_listen
        }
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()
