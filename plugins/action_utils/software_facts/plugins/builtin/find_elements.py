# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: find_elements
short_description: Find elements that match a filter from a given list.
description:
     - Find elements that match a filter from a given list.
     - It will return an empty list if nothing matches the specified filter.
     - If no filter is provided, all list elements will be returned
options:
  source:
    description:
      - The list where elements are stored
    type: list
    elements: dict
    required: true
  filter:
    description:
      - Filter to apply to the list elements
    type: dict
    required: false
    default: {}
'''

EXAMPLES = r'''
- name: Find in elements
  find_elements:
    source: list_dict
    filter:
      value: var1
  register: result
'''

import re  # noqa

from ansible.module_utils.six import iteritems  # noqa
from ansible.utils.display import Display  # noqa

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa

display = Display()


class FindElements(SoftwareFactsPlugin):

    @classmethod
    def get_name(cls):
        return super(FindElements, cls).get_name()

    @classmethod
    def get_args_spec(cls):
        args = super(FindElements, cls).get_args_spec()
        args.update(dict(
            source=dict(type='list', required=True),
            filter=dict(type='dict', required=False, default={})))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        source = args['source']

        filtered_elements = []
        for element in source:
            filters_match = True

            # Values given by the user could be of multiple types, but since we need to support matching regex,
            # we cast both of them to strings to do the comparison.
            for k, v in iteritems(args['filter']):
                k = self._templar.template(k)
                v = self._templar.template(v)

                if not validate_filter(element, k, v):
                    filters_match = False
                    break

            if filters_match:
                filtered_elements.append(element)

        return filtered_elements


def validate_filter(element, key, value):
    validated = True

    if key not in element:
        validated = False
    else:
        if isinstance(value, dict):
            for k, v in iteritems(value):
                if not validate_filter(element[key], k, v):
                    validated = False
                    break
        else:
            if not re.match(str(value), str(element[key])):
                validated = False

    return validated
