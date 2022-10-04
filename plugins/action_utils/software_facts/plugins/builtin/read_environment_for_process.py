# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: read_environment_for_process
short_description: Reads the environment vars attached to a process.
description:
     - Reads the environment vars attached to a process.
     - The process is defined using its pid.
options:
  pid:
    description:
      - PID of the process.
    type: str
    required: true
'''

EXAMPLES = r'''
- name: Read process environment
  read_environment_for_process:
    pid: '1234'
  register: env_vars
'''

RETURN = r'''
content:
    description: Plain text file content
    returned: success
    type: str
    sample: 'LANG=es_ES.UTF-8\x00PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin\x00'
source:
    description: Actual path of file slurped
    returned: success
    type: str
    sample: "/proc/1234/environ"
parsed:
    description: Parsed file content following provided parser and parser_params
    returned: success and parser provided
    type: dict
    sample: {"LANG": "es_ES.UTF-8", "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"}
'''

from ansible.utils.display import Display  # noqa: E402
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.read_remote_file \
    import ReadRemoteFile  # noqa: E402

display = Display()


class ReadEnvironmentForProcess(ReadRemoteFile):

    @classmethod
    def get_args_spec(cls):
        args = {}
        args.update(dict(
            pid=dict(type='str', required=True)))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        path = '/proc/{0}/environ'.format(args['pid'])
        result = super(ReadEnvironmentForProcess, self).run(
            dict(file_path=path, parser='environ', parser_params=None, in_docker=False, delegate_reading=False),
            attributes,
            software_instance)

        env_data = software_instance.get('docker', {}).get('full_data', {}).get('Config', {}).get('Env')
        if env_data:
            from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.utils \
                import get_software_facts_parser
            parser = get_software_facts_parser('key_value', self._action_module, self._task_vars)

            plain = '\n'.join(env_data)
            parsed = parser.parse(plain)

            if result.get('failed', False) is False:
                parsed.update(result['parsed'])
                plain = plain + '\n' + result['content']

            result['content'] = plain
            result['parsed'] = parsed

        return result
