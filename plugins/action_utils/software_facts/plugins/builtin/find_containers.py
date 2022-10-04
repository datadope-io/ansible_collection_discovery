# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: find_containers
short_description: Find containers inside the docker containers list.
description:
  - Looks for containers, filtering by the specified criteria and return the matching elements inside
    the docker containers list.
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
- name: Find containers
  find_containers:
    filter:
      container_name: "^cont*"
  register: result
'''


from ansible.utils.display import Display  # noqa

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.find_elements \
    import FindElements  # noqa

display = Display()


class FindContainers(FindElements):

    @classmethod
    def get_name(cls):
        return super(FindContainers, cls).get_name()

    @classmethod
    def get_args_spec(cls):
        args = super(FindContainers, cls).get_args_spec()
        del args['source']
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        dockers = self._task_vars.get('dockers', {})

        args['source'] = dockers.get('containers', [])

        return super(FindContainers, self).run(args, attributes, software_instance)
