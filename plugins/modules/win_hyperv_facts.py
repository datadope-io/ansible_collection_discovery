#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
---
module: win_hyperv_facts
version_added: '1.1.0'
short_description: Gather the Hyper-V virtual machines of the machine
description:
    - Gather the information of the Hyper-V virtual machines of the machine.
    - Extended information about the virtual machines can be gathered using a flag.
options:
  date_format:
    description:
      - Establishes the format of the date fields gathered.
      - Applies to the field creation_time
    type: str
    default: '%c'
  extended_data:
    description:
      - "By default, the module gathers: id, name, serial, hostname, network_adapters, path,
        creation_time, processor_count, memory, min_memory, max_memory, state and hypervisor.
        By setting this option to true, all the information related to the virtual machine is
        gathered, extending the module's output."
    type: bool
    default: false
notes:
- The extended_data flag is disabled by default as the gathered information that is
  collected by default is usually enough to achieve the goal of the module.
- Due to Hyper-V limitations, hostname of the virtual machines can only be obtained by doing a DNS search with each one
  of the VM's addresses.
author:
- David Nieto (@david-ns)
'''

EXAMPLES = r'''
- name: Gather Hyper-V facts
  datadope.discovery.win_hyperv_facts:

- name: Gather full processes facts
  datadope.discovery.win_hyperv_facts:
    extended_data: true

- name: Gather full processes facts with only the year within the date fields
  datadope.discovery.win_hyperv_facts:
    extended_data: true
    date_format: '%Y'
'''

RETURN = r'''
virtual_machines:
    description: List of dicts with the detected virtual machines
    returned: success
    type: list
    elements: dict
    sample: [
        {
            "creation_time": "ju. oct. 27 19:42:05 2022",
            "hostname": "vm1.mshome.net",
            "id": "f3abe0f9-3ba0-49a7-ae48-e2f0808cca9d",
            "max_memory": 1099511627776,
            "memory": 2147483648,
            "min_memory": 536870912,
            "name": "Ubuntu 18.04 LTS",
            "network_adapters": [
                {
                    "ip_addresses": [
                        "192.168.1.53",
                        "fe80::40:59c5:d1ca:b7e4"
                    ],
                    "is_management_os": false,
                    "mac_address": "00155D013902",
                    "name": "Network adapter",
                    "status": [
                        2
                    ],
                    "switch_name": "External switch"
                }
            ],
            "path": "C:\\ProgramData\\Microsoft\\Windows\\Hyper-V",
            "processor_count": 4,
            "serial": "4857-2270-1268-6889-7697-3920-09",
            "state": 2,
            "hypervisor": "Hyper-V"
        }
    ]
'''
