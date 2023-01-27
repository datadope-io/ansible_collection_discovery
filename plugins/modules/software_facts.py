#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: software_facts

short_description: Add list of detected software to ansible_facts.

version_added: "1.0.0"

description: Provides information of the configured software if it is found in the system.

options:
  software_list:
    description: List of software type configurations to discover.
    required: true
    type: list
    elements: dict
    suboptions:
      name:
        description: Name of the software to discover
        required: true
        type: str
      process_type:
        description: Type of process discovery with processes
        required: true
        type: str
        choices:
          - parent
          - child
      return_children:
        description: Return children processes if true
        required: false
        type: bool
        default: False
      cmd_regexp:
        description: Regex to apply on processes to detect this software
        required: true
        type: str
      pkg_regexp:
        description: Regex to apply to packages to detect this software
        required: true
        type: str
      return_packages:
        description: Return list of packages
        required: false
        type: bool
        default: False
      custom_tasks:
        description: Tasks to execute to enrich software returned information
        required: false
        type: list
        elements: dict
      vars:
        description: Variables to provide as task vars to the plugins executed by the provided tasks.
        required: false
        type: dict
  include_software:
    description:
      - List of software types to include from I(software_list).
      - Each element will match the I(name) field for each element of I(software_list) option.
      - If any element of the list is B(all), this option is omitted or is C(null), all the software types will be
        included except the ones explicitly indicated in I(exclude_software).
    required: false
    type: list
    elements: str
  exclude_software:
    description:
      - List of software types to exclude from I(software_list).
      - Each element will match the I(name) field for each element of I(software_list) option.
      - Software types in this list will never be processed.
    required: false
    type: list
    elements: str
  processes:
    description: List of processes running in the host.
    required: true
    type: list
    elements: dict
    suboptions:
      pid:
        description: PID of the process.
        required: true
        type: str
      ppid:
        description: Parent PID of the process.
        required: true
        type: str
      cmdline:
        description: Command line of the process.
        required: true
        type: str
      cwd:
        description: Working directory of the process.
        required: true
        type: str
  tcp_listen:
    description:
      - List of tcp ports listening in the host.
      - Empty list if no udp port is in listen state.
    required: true
    type: list
    elements: dict
  udp_listen:
    description:
      - List of udp ports listening in the host.
      - Empty list if no udp port is in listen state.
    required: true
    type: list
    elements: dict
  packages:
    description:
      - Packages installed in the target host as a dict.
      - Expected package format as module package_facts return.
      - Returned dict key is the package name, and value is a list of objects with packager info for every package version
    required: false
    type: dict
  dockers:
    description:
      - Information of every docker container running on the machine.
      - Provided information for each docker should be the same as one obtained with a docker inspect command.
    required: false
    type: dict
  pre_tasks:
    description:
      - List of plugins to execute with every discovered software instances.
      - These plugins will be executed before specific software type plugins.
    required: false
    type: list
    elements: dict
  post_tasks:
    description:
      - List of plugins to execute with every discovered software instances.
      - These plugins will be executed after specific software type plugins.
    required: false
    type: list
    elements: dict

author:
    - Datadope (@datadope)
'''

EXAMPLES = r'''
# List running software
- name: List running software
  datadope.discovery.software_facts: {}
'''

RETURN = r'''
ansible_facts:
  description: Facts to add to ansible_facts.
  returned: always
  type: dict
  contains:
    software:
        description: List of the detected software.
        returned: always
        type: list
        elements: dict
        contains:
          type:
            description: Name of the software type.
            returned: always
            type: str
          process:
            description: Discovered processes for the given software.
            returned: always
            type: dict
            contains:
                pid:
                    description: PID of the software process.
                    returned: always
                    type: str
                ppid:
                    description: Parent PID of the software process.
                    returned: always
                    type: str
                cmdline:
                    description: CMDLine of the software process.
                    returned: always
                    type: str
                listening_ports:
                    description: List of the ports where the software is listening.
                    type: list
                    elements: str
                children:
                    description: List of the child processes of the parent.
                    returned: when process_type is set to child
                    type: list
                    elements: dict
                    contains:
                        pid:
                            description: PID of the child.
                            returned: always
                            type: str
                        ppid:
                            description: Parent PID of the child.
                            returned: always
                            type: str
                        cmdline:
                            description: CMDLine of the child.
                            returned: always
                            type: str
                        listening_ports:
                            description: List of the ports where the software is listening.
                            type: list
                            elements: str
          listening_ports:
            description: List of the ports where the software is listening.
            type: list
            elements: int
          packages:
            description: List of packages info
            type: list
            elements: dict
            returned: if C(packages) is provided and return_packages is True
          version:
            description:
              - Information about version of software obtained in different ways.
            type: list
            elements: dict
            contains:
              type:
                description: Mechanism used to get the version
                type: str
                returned: always
              number:
                description: Version info
                type: str
                returned: always
          discovery_time:
            description:
              - Instant when Discovery was executed.
              - "With time format: yyyy-mm-ddTHH:MM:SS+0x:00."
            type: str
            returned: always
          docker:
            description: Information about the container that is running the software.
            type: dict
            returned: If software is installed as a docker container.
            contains:
              id:
                description: Docker container Id.
                type: str
                returned: always
              image:
                description: Docker container image (from container's Config.Image field).
                type: str
                returned: always
              name:
                description: Docker container Name.
                type: str
                returned: always
              exposed_ports:
                description: Docker container exposed ports (from container's Config.ExposedPorts field).
                type: dict
                returned: always
              network_mode:
                description: Docker container network mode (from container's HostConfig.NetworkMode field).
                type: str
                returned: always
              port_bindings:
                description: Docker container port bindings (from container's HostConfig.PortBindings field)
                type: dict
                returned: always
          files:
            description: List of files discovered for the software instance.
            type: list
            elements: dict
            contains:
              path:
                description:
                  - The full path of the file/object to store
                type: str
                returned: always
              name:
                description:
                  - The name of the file itself
                type: str
                returned: if a file name is available.
              type:
                description:
                  - "Type of the file to be stored. Ex: 'bin', 'config', etc."
                type: str
                returned: always
              subtype:
                description:
                  - A secondary type if it's needed due to multiple files of the same type
                type: str
              extra_data:
                description:
                  - A dict to store additional information about the file being returned.
                type: dict
                returned: if additional info is available.
          bindings:
            description:
              - List of bindings discovered for the software instance.
              - A binding is a connection point to the software conformed by an address and a port.
            type: list
            elements: dict
            contains:
              address:
                description:
                  - IP information of the object to add.
                type: str
              port:
                description:
                  - Port information of the object to add.
                type: str
              protocol:
                description:
                  - Protocol of the object to add.
                type: str
              class:
                description:
                  - Class type of the IP/port.
                type: str
                returned: always
              extra_data:
                description:
                  - A dict to store additional information about the file being returned.
                type: dict
                returned: if additional info is available.
          endpoints:
            description:
              - List of endpoints discovered for the software instance.
              - An endpoint is a connection point to the software conformed by an uri.
            type: list
            elements: dict
            contains:
              uri:
                description:
                  - The uri of the endpoint.
                type: str
                returned: always
              type:
                description:
                  - Type of the endpoint.
                type: str
                returned: always
              extra_data:
                description:
                  - A dict to store additional information about the file being returned.
                type: dict
                returned: if additional info is available.
          messages:
            description: List of messages sent by the remote host in the discovery process.
            type: list
            elements: dict
            contains:
              msg:
                description:
                  - The message to store.
                type: str
                returned: always
              key:
                description:
                  - A key to provide with the message to identify the problem
                type: str
                returned: If the message should be associated with a variable.
              value:
                description:
                  - A value for the key. Can be of any type of data
                type: complex
                returned: If the key field is returned.
              extra_data:
                description:
                  - A dict to store additional information about the message we are storing.
                type: dict
                returned: if additional info is available.
          extra_data:
            description:
              - Other information related to the precise software not having place in the other software fields.
              - Data is return as key/value pairs. Value may be of any type of data.
            type: dict
            returned: if additional info is available.

        sample: [
            {
                'name': 'PostgreSQL Database',
                'process':
                    {
                        'pid': '1234',
                        'ppid': '1',
                        'cmdline': '/usr/bin/postgres -D /var/lib/postgresql/data',
                        'listening_ports': [
                            '5432'
                        ],
                        'children': [
                            {
                                'pid': '1235',
                                'ppid': '1234',
                                'cmdline': 'postgres: logger process'
                            },
                            {
                                'pid': '1236',
                                'ppid': '1234',
                                'cmdline': 'checkpointer process'
                            }
                        ]
                    },
                'listening_ports': [
                    5432
                ],
                'packages': [
                    {
                        'arch': 'x86_64',
                        'epoch': None,
                        'name': 'postgresql10-server',
                        'release': '1PGDG.rhel7',
                        'source': 'rpm',
                        'version': '10.17'
                    }
                ],
                'version': [
                    {
                        'number': '10.17',
                        'type': 'package'
                    }
                ]
            }
        ]
'''
