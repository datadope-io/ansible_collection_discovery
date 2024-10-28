#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: connection_facts
version_added: '1.13.0'
short_description: Obtain a list of all current connections on a linux machine.
description: Provides information of the existing connections, including PID, process name and commandline.
options: {}
author:
- David Nieto (@david-ns)
'''

EXAMPLES = r'''
# List running processes
- name: List existing connections
  datadope.discovery.connection_facts: {}
'''

RETURN = r'''
ansible_facts:
  description: Facts to add to ansible_facts.
  returned: always
  type: dict
  contains:
    connections:
        description: List of connections.
        returned: always
        type: list
        elements: dict
        sample: [
            {
                "conn": [
                    "192.168.1.1:67"
                ],
                "listen": [
                    "192.168.1.204:68",
                    "fe80::5742:3e52:871a:2015:546"
                ],
                "meta": {
                    "cmdline": "/usr/sbin/NetworkManager --no-daemon",
                    "host": "david",
                    "process_name": "NetworkManager"
                }
            }
        ]
'''

import os  # noqa
import socket  # noqa

from ansible.module_utils.basic import AnsibleModule  # noqa
from ansible_collections.datadope.discovery.plugins.module_utils.psutil_net import NetConnections  # noqa


def group_connections_by_process(connections, processes):
    grouped_connections = {}

    for connection in connections:
        pid = connection['pid']
        process = processes.get(pid)

        # Check if the process died between connection and process gathering
        if not process:
            continue

        if pid not in grouped_connections:
            grouped_connections[pid] = {
                'conn': set(),
                'listen': set(),
                'meta': {
                    'cmdline': process['cmdline'],
                    'host': process['hostname'],
                    'process_name': process['exe']
                }
            }

        if connection['conn']:
            grouped_connections[pid]['conn'].add(connection['conn'])

        if connection['listen']:
            grouped_connections[pid]['listen'].add(connection['listen'])

    return list(grouped_connections.values())


def get_process_info():
    process_info = {}
    hostname = socket.gethostname()

    for pid in os.listdir('/proc'):
        if pid.isdigit():
            pid_path = os.path.join('/proc', pid)
            try:
                with open(os.path.join(pid_path, 'cmdline'), 'r') as f:
                    cmdline = f.read().replace('\0', ' ').strip()

                exe_path = os.readlink(os.path.join(pid_path, 'exe'))
                exe = os.path.basename(exe_path)

                process_info[pid] = {
                    'cmdline': cmdline,
                    'exe': exe,
                    'hostname': hostname.lower()
                }
            except Exception:
                # Ignore processes in which we're unable to gather information
                continue

    return process_info


def get_connections():
    net_connections = NetConnections()
    raw_connections = net_connections.retrieve('inet')

    processed_connections = []
    for connection in raw_connections:
        processed_connections.append({
            'conn': "%s:%s" % (connection.raddr) if connection.raddr else '',
            'listen': "%s:%s" % (connection.laddr),
            'status': connection.status,
            'pid': str(connection.pid)
        })

        pass

    return processed_connections


argument_spec = dict()


def setup_module_object():
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    return module


def main():
    result = dict(
        changed=False,
        ansible_facts=dict()
    )
    module = setup_module_object()

    connections = get_connections()
    processes = get_process_info()

    result['ansible_facts']['connections'] = group_connections_by_process(connections,
                                                                          processes)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
