# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: find_ports
short_description: Find ports inside the ports lists.
description:
  - Looks for ports, filtering by the specified criteria and return the matching elements inside
    the ports list.
  - Uses both UDP and TCP port lists.
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
- name: Find ports
  find_ports:
    filter:
      protocol: "udp"
      port: "3[0-9]{3}1"
  register: result
'''

from ansible.utils.display import Display  # noqa

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.find_elements \
    import FindElements  # noqa

display = Display()


class FindPorts(FindElements):

    @classmethod
    def get_name(cls):
        return super(FindPorts, cls).get_name()

    @classmethod
    def get_args_spec(cls):
        args = super(FindPorts, cls).get_args_spec()
        del args['source']
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        tcp_listen = self._task_vars.get('tcp_listen', [])
        udp_listen = self._task_vars.get('udp_listen', [])

        args['source'] = tcp_listen + udp_listen

        return super(FindPorts, self).run(args, attributes, software_instance)
