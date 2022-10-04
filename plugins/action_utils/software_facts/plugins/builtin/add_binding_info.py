# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
---
software_facts_plugin: add_binding_info
short_description: Usable for adding information to bindings
description:
    - This plugin is used to add information to the binding section. What is used to have address and port information
options:
  address:
    description:
      - IP information of the object to add.
    type: str
    required: False
  port:
    description:
      - Port information of the object to add.
    type: str
    required: False
  protocol:
    description:
      - Protocol of the object to add.
    type: str
    required: False
  class:
    description:
      - Class type of the IP/port. Default is 'service'.
    type: str
    required: False
    default: 'service'
  extra_data:
    description:
      - If it is necessary to add more information, it is added with key - value.
    type: dict
    required: False

notes:
  - Will check that at least 'address' or 'port' exists so that the plugin adds the information in bindings correctly.
author:
- Datadope
"""

EXAMPLES = r"""
- name: Add binding info
  add_binding_info:
    address: '0.0.0.0'
    port: 8080
    protocol: TCP
"""

from ansible.utils.display import Display  # noqa
from ansible.errors import AnsibleRuntimeError, AnsibleActionFail  # noqa
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa
from ansible.module_utils.six import iteritems  # noqa

display = Display()


class AddBindingInfo(SoftwareFactsPlugin):

    def __init__(self, action_module, task_vars):
        super(AddBindingInfo, self).__init__(action_module, task_vars)

    @classmethod
    def get_args_spec(cls):
        return {'address': {"type": 'str', "required": False},
                'port': {"type": 'int', "required": False},
                'protocol': {"type": 'str', "required": False},
                'class': {"type": 'str', "required": False, "default": "service"},
                'extra_data': {"type": 'dict', "required": False}}

    def validate_args(self, args):
        validated_args = super(AddBindingInfo, self).validate_args(args)
        if not validated_args.get('address') and not validated_args.get('port'):
            raise AnsibleRuntimeError("Wrong parameters sent to software facts plugin '{0}':\n{1}".
                                      format(self.get_name(), "Need address or port parameter"))
        return validated_args

    def run(self, args=None, attributes=None, software_instance=None):
        item_binding = {}
        for item, value in iteritems(args):
            if value:
                item_binding[item] = value
        result = dict(__instance__={'bindings': []}, __list_merge__='append')
        for binding in software_instance.get('bindings', []):
            if binding.get('address') == item_binding.get('address') \
                    and binding.get('port') == item_binding.get('port') \
                    and (binding.get('protocol') == item_binding.get('protocol') or not item_binding.get('protocol')):

                item_binding_class = item_binding.get('class')
                if item_binding_class is not None:
                    binding['class'] = item_binding_class

                item_binding_protocol = item_binding.get('protocol')
                if item_binding_protocol is not None:
                    binding['protocol'] = item_binding_protocol

                binding.setdefault('extra_data', {}).update(item_binding.get('extra_data', {}))
                return result
        result['__instance__']['bindings'].append(item_binding)
        return result
