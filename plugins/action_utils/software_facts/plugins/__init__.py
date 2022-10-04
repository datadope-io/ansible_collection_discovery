# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from abc import ABCMeta, abstractmethod

from ansible.errors import AnsibleRuntimeError
from ansible.module_utils.six import with_metaclass
from ansible.utils.display import Display

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.__init__ \
    import ArgumentSpecValidator

display = Display()


class SoftwareFactsPlugin(with_metaclass(ABCMeta, object)):
    def __init__(self, action_module, task_vars):
        self._action_module = action_module
        self._task_vars = task_vars
        self._task = action_module._task
        self._connection = action_module._connection
        self._play_context = action_module._play_context
        self._loader = action_module._loader
        self._templar = action_module._templar
        self._shared_loader_obj = action_module._shared_loader_obj

    @classmethod
    @abstractmethod
    def get_args_spec(cls):
        return {}

    @classmethod
    def get_name(cls):
        """
        Return name to use in software definition. Default implementation use camel case version of class name.
        """
        return cls.__module__.rsplit('.', maxsplit=1)[-1]

    @abstractmethod
    def run(self, args=None, attributes=None, software_instance=None):  # noqa
        return None

    def validate_args(self, args):
        """
        Raise exception in case the arguments don't pass validation.
        """
        validator = ArgumentSpecValidator(self.get_args_spec())
        validation_result = validator.validate(args)
        if validation_result.error_messages:
            raise AnsibleRuntimeError("Wrong parameters sent to software facts plugin '{0}':\n{1}".
                                      format(self.get_name(), '\n'.join(validation_result.error_messages)))
        return validation_result.validated_parameters

    def _execute_module(self, module_name=None, module_args=None, task_vars=None,
                        persist_files=False, wrap_async=False):
        return self._action_module.execute_module(module_name=module_name, module_args=module_args,
                                                  task_vars=task_vars, persist_files=persist_files,
                                                  wrap_async=wrap_async)

    def _display_v(self, msg):
        return self._action_module._display_v(msg)
