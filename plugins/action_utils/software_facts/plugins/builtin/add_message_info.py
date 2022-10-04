# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: add_message_info
short_description: Add a message to the instance message's dict.
description:
     - Insert a new message with its information into the message's dict, used to store information about messages sent
       by the remote host we are currently executing the discovery process..
options:
  msg:
    description:
      - The message to store
    type: str
    required: true
  key:
    description:
      - Key value specifying what is this message about in one word. Ex: 'connect', 'log'
    type: str
    required: false
  value:
    description:
      - A value adding information for the specified key. Can be of any type of data
    type: raw
    required: false
  extra_data:
    description:
      - A dict to store more information about the message we are storing.
    type: dict
    required: false
'''

EXAMPLES = r'''
 add_message_info:
    msg: Test message
    key: can_connect
    value: yes
    extra_data: {'any': any}
'''

from ansible.utils.display import Display  # noqa
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa: E402
from ansible.module_utils.six import iteritems  # noqa


display = Display()


class AddMessageInfo(SoftwareFactsPlugin):
    def __init__(self, action_module, task_vars):
        super(AddMessageInfo, self).__init__(action_module, task_vars)

    @classmethod
    def get_name(cls):
        return super(AddMessageInfo, cls).get_name()

    @classmethod
    def get_args_spec(cls):
        args = super(AddMessageInfo, cls).get_args_spec()
        args.update(dict(
            msg=dict(type='str', required=True)),
            key=dict(type='str', required=False),
            value=dict(type='raw', required=False),
            extra_data=dict(type='dict', required=False))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        message_info = {}
        for k, v in iteritems(args):
            if v:
                message_info[k] = v
        result = dict(__instance__={'messages': []}, __list_merge__='append')
        for message in software_instance.get('messages', []):
            if message.get('msg') == message_info.get('msg') and message.get('key') == message_info.get('key') \
                    and message.get('value') == message_info.get('value'):
                message.setdefault('extra_data', {}).update(message_info.get('extra_data', {}))
                return result
        result['__instance__']['messages'].append(message_info)
        return result
