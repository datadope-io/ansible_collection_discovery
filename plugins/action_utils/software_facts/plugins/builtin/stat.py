# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: stat
short_description: Retrieve file or file system status
description:
     - Retrieves facts for a file similar to the Linux/Unix 'stat' command.
options:
  path:
    description:
      - The full path of the file/object to get the facts of.
    type: path
    required: true
    aliases: [ dest, name ]
  follow:
    description:
      - Whether to follow symlinks.
    type: bool
    default: no
  get_mime:
    description:
      - Use file magic and return data about the nature of the file. this uses
        the 'file' utility found on most Linux/Unix systems.
      - This will add both C(mime_type) and C(charset) fields to the return, if possible.
      - In Ansible 2.3 this option changed from I(mime) to I(get_mime) and the default changed to C(yes).
    type: bool
    default: yes
    aliases: [ mime, mime_type, mime-type ]
    platform: "linux"
  get_attributes:
    description:
      - Get file attributes using lsattr tool if present.
    type: bool
    default: yes
    aliases: [ attr, attributes ]
    platform: "linux"
  in_docker:
    description:
      - Consider the paths are inside the docker containing the software.
      - If software is not detected to run in a docker this parameter is not used.
      - This parameter is ignored if platform is windows.
    type: bool
    default: yes
'''

EXAMPLES = r'''
- name: Check config file
  stat:
    path: "/etc/nginx/nginx.conf"
  register: conf_file_stat
'''

RETURN = r'''
stat:
    description:
        - Dictionary containing all the stat data, some platforms might add additional fields.
        - See ansible.builtin.stat and ansible.windows.win_stat for full object definition for each platform.
    returned: success
    type: complex
'''

from ansible.utils.display import Display  # noqa: E402
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa: E402

display = Display()


class Stat(SoftwareFactsPlugin):

    @classmethod
    def get_args_spec(cls):
        # One element dict with key the module name and value its arguments.
        args = dict(
            path=dict(type='path', required=True, aliases=['dest', 'name']),
            follow=dict(type='bool', default=False),
            get_mime=dict(type='bool', default=True, aliases=['mime', 'mime_type', 'mime-type']),
            get_attributes=dict(type='bool', default=True, aliases=['attr', 'attributes']),
            in_docker=dict(type='bool', required=False, default=True)
        )
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        path = args['path']

        is_windows = self._task_vars.get('ansible_facts', {}).get('os_family', '').lower().startswith('windows')

        in_docker = args['in_docker']
        if in_docker and not is_windows \
                and software_instance.get("docker", {}).get("name") \
                and software_instance.get('process', {}).get("pid"):
            path_prefix = "/proc/{0}/root".format(software_instance['process']['pid'])
            args['path'] = "{0}{1}".format(path_prefix, path)
        else:
            path_prefix = ''

        module_name = 'ansible.windows.win_stat' if is_windows else 'ansible.builtin.stat'
        module_args = dict(**args)
        module_args['get_checksum'] = False
        if is_windows:
            module_args.pop('get_mime', None)
            module_args.pop('get_attributes', None)
        module_args.pop('in_docker', None)

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
            stat_data = module_result['stat']
            exists = stat_data['exists']
            if not exists:
                msg = "Path '{0}' not found".format(path)
                display.v(msg)
                result['failed'] = True
                result['msg'] = msg
            else:
                stat_data['path'] = stat_data['path'][len(path_prefix):]
                result['failed'] = False
                result['stat'] = stat_data

        return result
