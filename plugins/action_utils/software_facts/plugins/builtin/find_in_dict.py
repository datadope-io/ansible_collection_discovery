# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: find_in_dict
short_description: Returns the list of values in the provided dict whose key is the provided item.
processing the source dict recursively
description:
     - This plugin returns the list of values in the provided dict whose key is the provided item.
     - Source dict is processed recursively so elements may match in dicts that are values of some main dict field.
options:
  source:
    description:
      - The dictionary in which we are trying to find the elements,
    type: dict
    required: true
  item:
    description:
      - The filter for the elements to match when performing the looking operation.
    type: str
    required: true
'''

EXAMPLES = r'''
- name: Find in dict
  find_in_dict:
    item: key3
    source:
      key1: value1
      key2: value2
      key3: value3
      other:
        key3: inner
  register: result  # result will store the list: ['value3', 'inner'].
'''

from ansible import constants as C  # noqa
from ansible.module_utils.six import iteritems  # noqa
from ansible.utils.display import Display  # noqa

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa

display = Display()


class FindInDict(SoftwareFactsPlugin):

    @classmethod
    def get_name(cls):
        return super(FindInDict, cls).get_name()

    @classmethod
    def get_args_spec(cls):
        args = super(FindInDict, cls).get_args_spec()
        args.update(dict(
            item=dict(type='str', required=True),
            source=dict(type='dict', required=True)))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        return get_recursively(source=args['source'],
                               item=args['item'])


def get_recursively(source, item):
    found = []

    for key, value in iteritems(source):
        if key == item:
            found.append(value)

        elif isinstance(value, dict):
            found.extend(get_recursively(value, item))

        elif isinstance(value, list):
            for element in value:
                if isinstance(element, dict):
                    found.extend(get_recursively(element, item))

    return found
