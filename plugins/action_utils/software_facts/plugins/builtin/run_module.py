# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: run_module
short_description: Executes the provided ansible module.
description:
     - This plugin executes the provided ansible module.
options:
  raw_dict:
    description:
      - Dict must have one and only one key.
      - The key is the module to execute.
      - The value will be the arguments to pass to the module .
    type: dict
    required: true
'''

EXAMPLES = r'''
- name: Check http or https
  run_module:
    check_connection:
      address: 127.0.0.1
      port: 3356
  register: response

- name: Request information from endpoint
  run_module:
    uri:
      url: 127.0.0.1
      method: "GET"
      body_format: "json"
      body:
        operation: "read-resource"
  register: response
'''

from ansible.errors import AnsibleRuntimeError  # noqa
from ansible.module_utils.six import iteritems, text_type  # noqa
from ansible.utils.display import Display  # noqa

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa: E402
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.run_command \
    import RunCommand  # noqa

display = Display()


class RunModule(SoftwareFactsPlugin):

    @classmethod
    def get_args_spec(cls):
        # One element dict with key the module name and value its arguments.
        args = super(RunModule, cls).get_args_spec()
        args.update(dict(
            key_value=dict(type='str', required=True)))
        return args

    def validate_args(self, args):
        if not isinstance(args, (dict, str)) or len(args) != 1:
            raise AnsibleRuntimeError("Wrong parameters sent to software facts plugin '{0}':\n{1}".
                                      format(self.get_name(), 'Argument must be a dict with only one element'))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        (module_name, module_args), = iteritems(args)

        if module_name == 'command':
            command_p = RunCommand(self._action_module, self._task_vars)
            if isinstance(module_args, text_type):
                module_args = dict(cmd=module_args)
            command_p.validate_args(module_args)
            return command_p.run(module_args, attributes, software_instance)

        if isinstance(module_args, text_type):
            module_args = dict(_raw_params=module_args)
        module_result = self._execute_module(
            module_name=module_name,
            module_args=module_args,
            task_vars=self._task_vars,
            wrap_async=self._task.async_val)
        return module_result
