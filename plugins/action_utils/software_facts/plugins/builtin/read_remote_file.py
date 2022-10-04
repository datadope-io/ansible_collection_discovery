# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: read_remote_file
short_description: Reads a file from the target host.
description:
     - Reads a file from the target host.
     - A parser may be defined to be applied to the content of the file.
options:
  file_path:
    description:
      - Path to the file to read.
    type: str
    required: true
  parser:
    description:
      - Type of parser to apply to the content
    type: str
    choices:
      - json
      - yaml
      - xml
      - key_value
      - environ
      - custom
    required: true
  parser_params:
    description:
      - Parameters to provide to the parser.
    type: dict
    required: false
  in_docker:
    description:
      - If C(false) file is read from host file system even if software instance is running in a docker container.
    type: bool
    required: false
    default: true
  delegate_reading:
    description:
      - "If C(true) this plugin will not read the file.
        File reading is delegated to the parser which must be a custom parser able to read files"
    type: bool
    required: false
    default: false
'''

EXAMPLES = r'''
- name: Read config file
  read_remote_file:
    file_path: "/path/to/file"
    parser: key_value
    parser_params:
      separators:
        - "="
      comment_delimiters:
        - "#"
        - "["
  register: result
'''

RETURN = r'''
content:
    description: Plain text file content
    returned: success
    type: str
    sample: "LANG=es_ES.UTF-8\nPATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin\n"
source:
    description: Actual path of file slurped
    returned: success
    type: str
    sample: "/path/to/file"
parsed:
    description: Parsed file content following provided parser and parser_params
    returned: success and parser provided
    type: dict
    sample: {"LANG": "es_ES.UTF-8", "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"}
'''

import base64  # noqa: E402
import traceback  # noqa: E402

from ansible.module_utils.common.text.converters import to_text  # noqa: E402
from ansible.utils.display import Display  # noqa: E402

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa: E402

display = Display()


class ReadRemoteFile(SoftwareFactsPlugin):

    @classmethod
    def get_args_spec(cls):
        args = super(ReadRemoteFile, cls).get_args_spec()
        args.update(dict(
            file_path=dict(type='str', required=True),
            parser=dict(type='str', required=False),
            parser_params=dict(type='dict', required=False),
            in_docker=dict(type='bool', required=False, default=True),
            delegate_reading=dict(type='bool', required=False, default=False)
        ))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        path = args['file_path']
        parser_name = args['parser']
        parser_params = args['parser_params']
        in_docker = args['in_docker']
        delegate_reading = args['delegate_reading']
        if parser_name:
            from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.utils \
                import get_software_facts_parser
            parser = get_software_facts_parser(parser_name, self._action_module, self._task_vars)
        else:
            parser = None

        path_prefix = ''
        if in_docker \
                and software_instance.get("docker", {}).get("name") \
                and software_instance.get('process', {}).get("pid"):
            # Executing in docker
            path_prefix = "/proc/{0}/root".format(software_instance['process']['pid'])
            path = "{0}{1}".format(path_prefix, path)

        result = {}
        source = path

        if not delegate_reading:
            result = self._execute_module(module_name='ansible.legacy.slurp',
                                          module_args=dict(src=path),
                                          task_vars=self._task_vars)
            if result.get('failed', False):
                if 'not found' in result.get('msg', ''):
                    msg = "the remote file '{0}' does not exist, not transferring".format(path)
                elif result.get('msg', '').startswith('source is a directory'):
                    msg = "remote file is a directory"
                else:
                    msg = result.get('msg', '')
                result['msg'] = msg
            else:
                if result['encoding'] == 'plain':  # Impossible from real module but included to facilitate mocking
                    source = to_text(result['content'])
                else:
                    source = to_text(base64.b64decode(result['content']))
                result['content'] = source
                del result['encoding']

        if parser:
            try:
                parser.validate_input(source, parser_params)
                parsed_file = parser.parse(source, parser_params, path_prefix)
                if delegate_reading:
                    # If we are delegating the reading, we need to extract the parsed file from the delegated
                    # task output. Also, we need to add the source to the result as slurp does.
                    result['parsed'] = parsed_file['parsed']
                    result['source'] = path
                else:
                    result['parsed'] = parsed_file
            except Exception as e:
                if display.verbosity > 2:
                    display.verbose(
                        "Error '{0}' parsing to '{1}' text {2}".format(str(e), parser_name, source),
                        host=self._task_vars.get('inventory_hostname'))
                else:
                    display.v(
                        "Error '{0}' parsing text to '{1}'".format(str(e), parser_name),
                        host=self._task_vars.get('inventory_hostname'))
                result['failed'] = True
                result['msg'] = str(e)
                result['exception'] = traceback.format_exc()

        return result
