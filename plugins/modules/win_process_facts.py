#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
---
module: win_process_facts
version_added: '1.11.0'
short_description: Gather the facts of the current processes of the machine
description:
    - Gather the information of the running processes of the machine and
      the user that owns them.
options:
  date_format:
    description:
      - Establishes the format of the date fields gathered when the extended_data option
        is set.
      - "Applies to the following fields: creation_date, install_date and termination_date."
    type: str
    default: '%c'
  extended_data:
    description:
      - "By default, the module gathers: cmdline, pid, ppid and user. By setting
        this option to true, all the information related to the process is gathered,
        extending the module's output."
    type: bool
    default: false
notes:
- The extended_data flag is disabled by default as the gathered information that is
  collected by default is usually enough to achieve the goal of the module.
author:
- David Nieto (@david-ns)
'''

EXAMPLES = r'''
- name: Gather processes facts
  community.windows.win_process_facts:

- name: Gather full processes facts
  community.windows.win_process_facts:
    extended_data: true

- name: Gather full processes facts with only the year within the date fields
  community.windows.win_process_facts:
    extended_data: true
    date_format: '%Y'
'''

RETURN = r'''
processes:
    description: List of dicts with the processes of the machine
    returned: success
    type: list
    elements: dict
    sample: [
        {
            "cmdline": "\"C:\\Program Files\\Microsoft SQL Server\\MSSQL14.SQLEXPRESS\\MSSQL\\Binn\\sqlservr.exe",
            "pid": 1560,
            "ppid": 444,
            "user": "NT SERVICE\\MSSQL$SQLEXPRESS"
        }
    ]
'''
