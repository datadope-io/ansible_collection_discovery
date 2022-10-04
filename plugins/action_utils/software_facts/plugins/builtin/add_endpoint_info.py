# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: add_endpoint_info
short_description: Add an endpoint to the instance endpoint's dict
description:
     - Insert a new endpoint with its information into the endpoint's dict, used to store information about endpoints
       discovered through the discovery process.
options:
  uri:
    description:
      - The uri of the endpoint, consisting of 'http'/'https' + 'ip' + 'port'
    type: str
    required: true
  type:
    description:
      - Type of the endpoint.
    type: str
    required: false
    default: generic
  extra_data:
    description:
      - A dict to store more information about the endpoint we are storing in.
    type: dict
    required: false
'''

EXAMPLES = r'''
 add_endpoint_info:
    uri: 127.0.0.1:8080
    type: generic
    extra_data: {'active': yes}
'''

from ansible.utils.display import Display  # noqa
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa: E402
from ansible.module_utils.six import iteritems  # noqa


display = Display()


class AddEndpointInfo(SoftwareFactsPlugin):

    def __init__(self, action_module, task_vars):
        super(AddEndpointInfo, self).__init__(action_module, task_vars)

    @classmethod
    def get_name(cls):
        return super(AddEndpointInfo, cls).get_name()

    @classmethod
    def get_args_spec(cls):
        args = super(AddEndpointInfo, cls).get_args_spec()
        args.update(dict(
            uri=dict(type='str', required=True),
            type=dict(type='str', required=False, default='generic'),
            extra_data=dict(type='dict', required=False)))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        endpoint_info = {}
        for k, v in iteritems(args):
            if v:
                endpoint_info[k] = v
        result = dict(__instance__={'endpoints': []}, __list_merge__='append')
        for endpoint in software_instance.get('endpoints', []):
            if endpoint.get('uri') == endpoint_info.get('uri'):

                endpoint_info_type = endpoint_info.get('type')
                if endpoint_info_type is not None:
                    endpoint['type'] = endpoint_info_type

                endpoint.setdefault('extra_data', {}).update(endpoint_info.get('extra_data', {}))
                return result
        result['__instance__']['endpoints'].append(endpoint_info)
        return result
