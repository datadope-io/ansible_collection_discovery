# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: parse
short_description: Provides a JSON representation of a content given a parser type
description:
     - Provides a JSON representation of a content given a parser type
options:
  content:
    description:
      - Content to parse
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
'''

EXAMPLES = r'''
- name: Parse json string
  parse:
    content: '{"key1": "value1", "key2", "value2"}'
    parser: "json"
  register: json_data
'''

RETURN = r'''
parsed:
    description: Parsed content following provided parser and parser_params
    returned: always
    type: dict
    sample: {"key1": "value1", "key2", "value2"}
'''

import traceback  # noqa: E402

from ansible.utils.display import Display  # noqa: E402

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa: E402

display = Display()


class Parse(SoftwareFactsPlugin):

    @classmethod
    def get_args_spec(cls):
        args = super(Parse, cls).get_args_spec()
        args.update(dict(
            content=dict(type='str', required=True),
            parser=dict(type='str', required=True),
            parser_params=dict(type='dict', required=False)
        ))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        source = args['content']
        parser_name = args['parser']
        parser_params = args['parser_params']

        from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.utils \
            import get_software_facts_parser
        parser = get_software_facts_parser(parser_name, self._action_module, self._task_vars)

        result = {}

        try:
            parser.validate_input(source, parser_params)
            parsed_file = parser.parse(source, parser_params)
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
