from abc import ABCMeta, abstractmethod

from ansible.module_utils.six import with_metaclass
from ansible.utils.display import Display

display = Display()


class SoftwareFactsParser(with_metaclass(ABCMeta, object)):
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
    def get_name(cls):
        """
        Return name to use in software definition. Default implementation use camel case version of class name.
        """
        return cls.__module__.rsplit('.', maxsplit=1)[-1]

    @abstractmethod
    def validate_input(self, source, config):
        """
        Validates if the source and config are valid for the parser.
        """
        return None

    @abstractmethod
    def parse(self, source, config=None, path_prefix=''):  # noqa
        return None

    def _execute_module(self, module_name=None, module_args=None, task_vars=None,
                        persist_files=False, wrap_async=False):
        return self._action_module.execute_module(module_name=module_name, module_args=module_args,
                                                  task_vars=task_vars, persist_files=persist_files,
                                                  wrap_async=wrap_async)
