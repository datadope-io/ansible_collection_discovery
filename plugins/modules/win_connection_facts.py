#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
---
module: win_connection_facts
version_added: '1.13.0'
short_description: Obtain a list of all current connections on a windows machine.
description: Provides information of the existing connections, including PID, process name and commandline.
options: {}
author:
- David Nieto (@david-ns)
'''

EXAMPLES = r'''
# List running processes
- name: List existing connections
  datadope.discovery.win_connection_facts: {}
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
                    "2606:2800:233:fa02:67b:9ff6:6107:833:80",
                    "2603:1026:2407::5:443"
                ],
                "listen": [
                    ":::51576",
                    ":::51575",
                    ":::51574",
                    "2a0c:5a85:e808:300:4493:4a5b:b414:630a:51575",
                    "2a0c:5a85:e808:300:4493:4a5b:b414:630a:51574"
                ],
                "meta": {
                    "cmdline": "\"C:\\Program Files\\WindowsApps\\HxOutlook.exe\" -ServerName:microsoft.windowslive.mail.App.mca",
                    "host": "david",
                    "process_name": "HxOutlook"
                }
            }
        ]
'''
