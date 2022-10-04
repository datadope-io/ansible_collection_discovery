# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: del_instance_fact
short_description: Removes a list of variables if present in the instance.
description:
     - Remove a variable or a list of variables given their names from the instance.
     - It will do nothing with those given names that doesn't match a variable present in the instance
options:
  keys:
    description:
      - The names of the elements to remove. At least one required
    type: list
    required: true
'''

EXAMPLES = r'''
- name: Remove temporary vars
  del_instance_fact:
    - var_temporary_1
    - var_temporary_2
'''

import ansible.constants as C  # noqa
from ansible.errors import AnsibleActionFail, AnsibleRuntimeError  # noqa
from ansible.module_utils.six import string_types  # noqa
from ansible.utils.display import Display  # noqa

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa

display = Display()


class DelInstanceFact(SoftwareFactsPlugin):

    def __init__(self, action_module, task_vars):
        super(DelInstanceFact, self).__init__(action_module, task_vars)

    @classmethod
    def get_args_spec(cls):
        # List of facts to remove
        return dict(keys=dict(type='list', required=True))

    def validate_args(self, args):
        if not isinstance(args, list):
            raise AnsibleRuntimeError("Wrong parameters sent to software facts plugin '{0}':\n{1}".
                                      format(self.get_name(), 'Argument must be a list'))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        if args:
            result = dict(deleted_from_instance=[])
            if isinstance(args, string_types):
                args = [args]
            for k in args:
                k = self._templar.template(k)
                dict_ = software_instance
                parts = k.split('.')
                last = parts[-1]
                for path in parts[:-1]:
                    if path in dict_:
                        dict_ = dict_[path]
                    else:
                        dict_ = None
                        break

                if dict_ and last in dict_:
                    del (dict_[last])
                    result['deleted_from_instance'].append(k)
            return result
        else:
            raise AnsibleActionFail('No keys provided, at least one is required for this action to succeed')
