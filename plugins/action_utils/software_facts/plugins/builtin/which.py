# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
software_facts_plugin: which
short_description: Return the file info if file exists in the provided paths.
description:
     - Return the file info if file exists in the provided paths.
options:
    name:
        default: []
        description:
            - File name to search in provided I(paths)
        type: str
        required: true
    paths:
        description:
            - List of paths of directories to search. All paths must be fully qualified.
        type: list
        required: true
        elements: str
    hidden:
        description:
            - Set this to C(yes) to include hidden files, otherwise they will be ignored.
        type: bool
        default: no
    in_docker:
        description:
            - Consider the paths are inside the docker containing the software.
            - If software is not detected to run in a docker this parameter is not used.
            - This parameter is ignored if platform is windows.
        type: bool
        default: yes
    windows_valid_extensions:
        description:
            - Valid extensions to consider a file as an executable.
            - This parameter is ignored if platform is not windows.
        type: list
        elements: str
        default: ['.bat', '.bin', '.cmd', '.com', '.exe', '.ps1']
'''

EXAMPLES = r'''
- name: Run which
  which:
    name: file_name
    paths:
     - /etc
     - /var/etc
  register: result
'''

RETURN = r'''
file:
    description: The matched file data (see I(stat) module for full output of each dictionary)
    returned: success
    type: dict
    sample: {
        path: "/var/tmp/test1",
        mode: "0644",
        "...": "..."
        }
'''

from ansible.module_utils.six import text_type  # noqa: E402
from ansible.utils.display import Display  # noqa: E402
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa: E402

DEFAULT_WINDOWS_EXECUTABLE_EXTENSIONS = [
    '.bat', '.bin', '.cmd', '.com', '.exe', '.ps1'
]

display = Display()


class Which(SoftwareFactsPlugin):

    @classmethod
    def get_args_spec(cls):
        # One element dict with key the module name and value its arguments.
        args = dict(
            name=dict(type='str', required=True),
            paths=dict(type='list', elements='path', required=True),
            hidden=dict(type='bool', required=False, default=False),
            in_docker=dict(type='bool', required=False, default=True),
            windows_valid_extensions=dict(type='list', elements='str', required=False)
        )
        return args

    def run(self, args=None, attributes=None, software_instance=None):  # noqa
        name = args['name']
        paths = args['paths']
        if isinstance(paths, text_type):
            paths = [paths]

        is_windows = self._task_vars.get('ansible_facts', {}).get('os_family', '').lower().startswith('windows')

        in_docker = args['in_docker']
        if in_docker and not is_windows \
                and software_instance.get("docker", {}).get("name") \
                and software_instance.get('process', {}).get("pid"):
            path_prefix = "/proc/{0}/root".format(software_instance['process']['pid'])
            paths_to_use = []
            for path in paths:
                paths_to_use.append("{0}{1}".format(path_prefix, path))
        else:
            paths_to_use = paths
            path_prefix = ''

        module_name = 'ansible.windows.win_find' if is_windows else 'ansible.builtin.find'
        module_args = dict(patterns=name, paths=paths_to_use, recurse=False, use_regex=False,
                           file_type='file', hidden=args['hidden'])

        module_result = self._execute_module(
            module_name=module_name,
            module_args=module_args,
            task_vars=self._task_vars,
            wrap_async=self._task.async_val)
        display.debug("RESULT FROM '{1}': {0}".format(module_result, module_name))
        result = {}
        if module_result.get('failed', False):
            display.v("Module '{1}' returned failed with message '{0}".format(result.get('msg', ''), module_name))
            result['failed'] = True
            result['msg'] = module_result.get('msg', "Undefined error executed module '{0}'".format(module_name))
            if 'exception' in module_result:
                result['exception'] = module_result['exception']
        else:
            if module_result['matched'] == 0:
                msg = "No file found with name '{0}' in '{1}'".format(name, paths_to_use)
                display.v(msg)
                result['failed'] = True
                result['msg'] = msg
            else:
                exe_extensions = args['windows_valid_extensions'] or DEFAULT_WINDOWS_EXECUTABLE_EXTENSIONS
                if is_windows:
                    files = [f for f in module_result['files']
                             if not f['isdir'] and f['extension'].lower() in exe_extensions]
                else:
                    files = [f for f in module_result['files']
                             if not f['isdir'] and any((f['xoth'], f['xgrp'], f['xusr']))]
                if not files:
                    msg = "No file found with right attributes for name '{0}' in '[{1}]'" \
                        .format(name, ', '.join(paths_to_use))
                    display.v(msg)
                    result['failed'] = True
                    result['msg'] = msg
                else:
                    result['failed'] = False
                    result['file'] = files[0]
                    result['file']['path'] = result['file']['path'][len(path_prefix):]

        return result
