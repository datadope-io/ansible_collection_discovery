#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Datadope, S.L. <info@datadope.io> (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: process_facts

short_description: Add list of running processes to ansible_facts.

version_added: "1.0.0"

description: Provides information of the running proceses, including PID, PPID, user and command line.

options: {}

author:
    - Datadope (@datadope)
'''

EXAMPLES = r'''
# List running processes
- name: List running processes
  datadope.discovery.processes_info: {}
'''

RETURN = r'''
ansible_facts:
  description: Facts to add to ansible_facts.
  returned: always
  type: dict
  contains:
    processes:
        description: List of running processes.
        returned: always
        type: list
        elements: dict
        contains:
          pid:
            description: PID of the process.
            returned: always
            type: str
          ppid:
            description: Parent PID of the process.
            returned: always
            type: str
          user:
            description: User which is owner of the process.
            returned: always
            type: str
          cmdline:
            description: Command line of the process.
            returned: always
            type: str
          cwd:
            description: Working directory of the process.
            returned: always
            type: str
        sample: [
          {
            'pid': '10',
            'ppid': '1',
            'user': 'root',
            'cmdline': 'the process command line',
            'cwd': '/'
          }
        ]
'''

import codecs  # noqa
import os  # noqa
import pwd  # noqa
import re  # noqa
import sys  # noqa

from ansible.module_utils.basic import AnsibleModule  # noqa
from ansible.module_utils.six import iteritems  # noqa


def utf8replace(ex):
    # The error handler receives the UnicodeDecodeError, which contains arguments of the
    # string and start/end indexes of the bad portion.
    bstr, start, end = ex.object, ex.start, ex.end

    # The return value is a tuple of Unicode string and the index to continue conversion.
    # Note: iterating byte strings returns int on 3.x but str on 2.x
    return u''.join('\\x{0:02x}'.format(c if isinstance(c, int) else ord(c))
                    for c in bstr[start:end]), end


codecs.register_error('utf8replace', utf8replace)  # noqa


def get_os_processes_default(module):  # noqa
    processes = []
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
        try:
            with open(os.path.join('/proc', pid, 'cmdline'), 'rb') as f:
                content = f.read()
                try:
                    cmdline = content.decode('ascii')
                except (UnicodeDecodeError, UnicodeTranslateError):
                    cmdline = content.decode("utf-8", "utf8replace")
                cmdline = cmdline.replace("\x00", " ").rstrip()
                if not isinstance(cmdline, str):  # in Python 2 it will be unicode
                    cmdline = cmdline.encode('utf-8')
            with open("/proc/%s/status" % pid) as f:
                status = f.read()
                ppid = re.findall(r"Ppid:\s+(\d+)", status, re.MULTILINE | re.I | re.DOTALL)[0]
                uid = re.findall(r"Uid:\s+(\d+)", status, re.MULTILINE | re.I | re.DOTALL)[0]
            cwd = os.readlink("/proc/%s/cwd" % pid)
            try:
                user = pwd.getpwuid(int(uid)).pw_name
            except KeyError:
                user = str(uid)
            processes.append({"pid": pid, "ppid": ppid, "user": user, "cmdline": cmdline, "cwd": cwd})
        except (IOError, OSError):  # proc has already terminated
            continue
    return processes


def _get_pid_cwd(module, pid):
    command = "pwdx %s" % pid
    rc, stdout, stderr = module.run_command(args=command,
                                            use_unsafe_shell=True)
    cwd = None
    if rc == 0:
        cwd = re.findall(r"%s:(.*?)$" % pid, stdout, re.MULTILINE | re.I | re.DOTALL)[0].strip()
    return cwd


def _process_ps_command_stdout(module, command):
    processes = []
    rc, stdout, stderr = module.run_command(args=command,
                                            use_unsafe_shell=True)
    if rc == 0:
        for line in stdout.splitlines():
            process = re.findall(r"([\d-]+)\s+([\d-]+)\s+(.*?)\s+(.*)", line.strip(), re.DOTALL)
            if process:
                pid, ppid, user, cmdline = process[0]
                cwd = _get_pid_cwd(module, pid)
                processes.append({"pid": pid, "ppid": ppid, "user": user, "cmdline": cmdline, "cwd": cwd})
    return processes


def get_os_processes_hpux(module):
    return _process_ps_command_stdout(module, "UNIX95= ps -e -o pid= -o ppid= -o user= -oargs= -x")


def get_os_processes_aix(module):
    return _process_ps_command_stdout(module, "ps -e -o pid= -o ppid= -o user= -o args=")


def get_os_processes_sunos(module):
    return _process_ps_command_stdout(module, "ps -e -o pid= -o ppid= -o user= -o args=")


_PROCESS_SPECIFIC_IMPLEMENTATIONS = {
    'hp-ux': get_os_processes_hpux,
    'aix': get_os_processes_aix,
    'sunos': get_os_processes_sunos
}

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


def get_os_processes(module):
    check_mode = module.check_mode
    if check_mode:
        return None
    platform = sys.platform

    process_func = get_os_processes_default
    for platform_spec, platform_func in iteritems(_PROCESS_SPECIFIC_IMPLEMENTATIONS):
        if platform_spec in platform:
            process_func = platform_func
            break

    return process_func(module)


def main():
    result = dict(
        changed=False,
        ansible_facts=dict()
    )
    module = setup_module_object()
    validate_parameters(module.params)
    # Make main process method independent of ansible objects to facilitate tests (if possible)
    processes = get_os_processes(module=module)
    if processes is not None:
        result['ansible_facts'] = {"processes": processes}
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()
