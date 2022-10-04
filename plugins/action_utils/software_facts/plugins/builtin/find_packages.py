# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: find_packages
short_description: Find packages inside the packages list.
description:
  - Looks for packages, filtering by the specified criteria and return the matching elements inside
    the packages list.
  - It will return an empty list if nothing matches the specified filter.
  - If no filter is provided, all elements are returned.
options:
  filter:
    description:
      - The filter for the elements to match when performing the operation.
    type: dict
    required: false
    default: {}
'''

EXAMPLES = r'''
- name: Find package
  find_packages:
    filter:
      name: "test"
  register: result
'''

from ansible.utils.display import Display  # noqa

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.find_elements \
    import FindElements  # noqa

display = Display()


class FindPackages(FindElements):

    @classmethod
    def get_name(cls):
        return super(FindPackages, cls).get_name()

    @classmethod
    def get_args_spec(cls):
        args = super(FindPackages, cls).get_args_spec()
        del args['source']
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        packages = self._task_vars.get('packages', {})

        # Since packages follows a schema like: {'foo': [{'name': 'foo', ...}, ...], 'bar': [{'name': 'bar', ...}, ...]}
        # we need to flatten it to a list of dicts. No information is lost since keys at first level are contained
        # in the dicts inside their values as the key 'name'.
        args['source'] = sum(packages.values(), [])

        return super(FindPackages, self).run(args, attributes, software_instance)
