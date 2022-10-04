# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
---
software_facts_plugin: set_instance_fact
short_description: Stores variables in the software instance return data.
description:
    - Stores variables in the software instance return data.
options:
  key_value:
    description:
      - Dictionary with keys to store with their values.
    type: dict
    required: True
"""

EXAMPLES = r"""
    - name: Store variables in instance
      set_instance_fact:
        name_var1: value1
        name_var2: value2
        name_var3: value3
"""

import ansible.constants as C  # noqa
from ansible.errors import AnsibleActionFail, AnsibleRuntimeError
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.module_utils.six import iteritems, string_types
from ansible.utils.display import Display
from ansible.utils.vars import isidentifier

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa: E402

display = Display()


class SetInstanceFact(SoftwareFactsPlugin):

    def __init__(self, action_module, task_vars):
        super(SetInstanceFact, self).__init__(action_module, task_vars)

    @classmethod
    def get_args_spec(cls):
        # Dict of facts to create and their values
        return dict(key_value=dict(type='dict', required=True))

    def validate_args(self, args):
        if not isinstance(args, dict):
            raise AnsibleRuntimeError("Wrong parameters sent to software facts plugin '{0}':\n{1}".
                                      format(self.get_name(), 'Argument must be a dict'))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        facts = {}
        if args:
            for (k, v) in iteritems(args):
                k = self._templar.template(k)

                if not isidentifier(k):
                    raise AnsibleActionFail(
                        "The variable name '%s' is not valid. "
                        "Variables must start with a letter or underscore character, "
                        "and contain only letters, numbers and underscores." % k)

                # NOTE: this should really use BOOLEANS from convert_bool, but only in the k=v case,
                # right now it converts matching explicit YAML strings also when 'jinja2_native' is disabled.
                if not C.DEFAULT_JINJA2_NATIVE and isinstance(v, string_types) and v.lower() in (  # noqa
                        'true', 'false', 'yes', 'no'):
                    v = boolean(v, strict=False)
                facts[k] = v
            return dict(__instance__=facts)
        else:
            raise AnsibleActionFail('No key/value pairs provided, at least one is required for this action to succeed')
