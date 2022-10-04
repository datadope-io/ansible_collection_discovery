# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleRuntimeError

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.parsers.__init__ \
    import SoftwareFactsParser


class CustomParser(SoftwareFactsParser):

    def validate_input(self, source, config):
        """
        Validate the input before parsing.
        """
        if config is None:
            raise AnsibleRuntimeError("No config provided for the custom parser when required.")
        if 'module_name' not in config:
            raise AnsibleRuntimeError("No module_name provided in config for the custom parser when required.")
        if 'module_args' in config and not isinstance(config['module_args'], dict):
            raise AnsibleRuntimeError("module_args must be a dict if given to custom parser.")

    def parse(self, source, config=None, path_prefix=''):
        """
        Parse the file located at the given source. The source in injected with the name 'file_path' to the module_args
        """
        module_name = config['module_name']
        module_args = config.get('module_args', {})

        if 'file_path' in module_args:
            raise AnsibleRuntimeError("The file_path argument is reserved for the custom parser.")

        module_args['file_path'] = source
        module_args['path_prefix'] = path_prefix

        module_result = self._execute_module(
            module_name=module_name,
            module_args=module_args,
            task_vars=self._task_vars,
            wrap_async=self._task.async_val)

        return module_result
