# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: run_command
short_description: Executes a command on the target host.
description:
     - This plugin executes a command on the target host, using ansible's command module.
     - "It manages if the software instance is running in a docker container.
       If that is the case, then executes the command in the container."
options:
  cmd:
    description:
      - Full command to execute.
    type: str
    required: false
  argv:
    description:
      - Command and arguments provided as a list.
    type: list
    required: false
  in_docker:
    description:
      - If C(false) command is executed in host even if software instance is running in a docker container.
    type: bool
    required: false
    default: true
'''

EXAMPLES = r'''
- name: Run command using cmd
  run_command:
    cmd: "postgres -V"
  register: result

- name: Run command using argv
  run_command:
    argv:
      - postgres
      - "-V"
  register: result
'''

from ansible.errors import AnsibleRuntimeError  # noqa
from ansible.module_utils.six import iteritems  # noqa
from ansible.utils.display import Display  # noqa

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa: E402

display = Display()


class RunCommand(SoftwareFactsPlugin):

    @classmethod
    def get_args_spec(cls):
        # One element dict with key the module name and value its arguments.
        args = dict(
            cmd=dict(type='str', required=False),
            argv=dict(type='list', required=False),
            in_docker=dict(type='bool', required=False, default=True)
        )
        return args

    def validate_args(self, args):
        validated_args = super(RunCommand, self).validate_args({x: y for x, y in iteritems(args)
                                                                if x in self.get_args_spec().keys()})
        # We have to update the args dict with the validated ones in order to keep additional args not specified
        # in the arguments specification
        args.update(validated_args)

        if not args['cmd'] and not args['argv']:
            raise AnsibleRuntimeError("Wrong parameters sent to software facts plugin '{0}':\n{1}".
                                      format(self.get_name(), "One of 'cmd' or 'argv' must be provided"))
        if args['cmd'] and args['argv']:
            raise AnsibleRuntimeError("Wrong parameters sent to software facts plugin '{0}':\n{1}".
                                      format(self.get_name(), "Only one of 'cmd' or 'argv' must be provided"))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        module_name = 'command'
        module_args = {}
        for key, value in iteritems(args):
            if key == 'cmd' and value:
                module_args['_raw_params'] = value
            # Avoid adding to module_args unnecessary arguments with default values
            elif key == 'cmd' or key == 'in_docker':
                continue
            else:
                module_args[key] = value

        in_docker = args['in_docker']
        if in_docker \
                and software_instance.get("docker", {}).get("name") \
                and software_instance.get('process', {}).get("pid"):
            # Executing in docker
            command_prefix = "nsenter -t {0} -m -u -n -p".format(software_instance['process']['pid'])
            if '_raw_params' in module_args:
                module_args['_raw_params'] = "{0} {1}".format(command_prefix, module_args['_raw_params'])
            else:
                module_args['argv'] = command_prefix.split(' ') + module_args['argv']

        module_result = self._execute_module(
            module_name=module_name,
            module_args=module_args,
            task_vars=self._task_vars,
            wrap_async=self._task.async_val)
        return module_result
