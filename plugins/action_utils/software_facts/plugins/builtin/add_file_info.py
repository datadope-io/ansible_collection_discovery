# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: add_file_info
short_description: Add a file to the instance file's dict
description:
     - Insert a new file with its information into the file's dict, used to store information about files used by
       the discovery process.
options:
  path:
    description:
      - The full path of the file/object to store
    type: str
    required: true
  type:
    description:
      - Type of the file to be stored. Ex: 'bin', 'config', etc.
    type: str
    required: true
  name:
    description:
      - The name of the file itself
    type: str
    required: false
  subtype:
    description:
      - A secondary type if it's needed due to multiple files of the same type
    type: str
    required: false
  extra_data:
    description:
      - A dict to store more information about the file we are storing.
    type: dict
    required: false
'''

EXAMPLES = r'''
 add_file_info:
    path: etc/nginx/nginx.conf
    type: config
    name: nginx.conf
    subtype: generic
    extra_data: {'raw': yes}
'''


from ansible.utils.display import Display  # noqa: E402
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa: E402
from ansible.module_utils.six import iteritems  # noqa: E402

display = Display()


class AddFileInfo(SoftwareFactsPlugin):
    def __init__(self, action_module, task_vars):
        super(AddFileInfo, self).__init__(action_module, task_vars)

    @classmethod
    def get_name(cls):
        return super(AddFileInfo, cls).get_name()

    @classmethod
    def get_args_spec(cls):
        args = super(AddFileInfo, cls).get_args_spec()
        args.update(dict(
            path=dict(type='str', required=True),
            type=dict(type='str', required=True),
            name=dict(type='str', required=False),
            subtype=dict(type='str', required=False),
            extra_data=dict(type='dict', required=False)))
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        file_info = {}
        for k, v in iteritems(args):
            if v:
                file_info[k] = v
        result = dict(__instance__={'files': []}, __list_merge__='append')
        for files in software_instance.get('files', []):
            if files.get('path') == file_info.get('path') and files.get('type') == file_info.get('type') and files.get(
                    "subtype") == file_info.get('subtype') and files.get('name') == file_info.get('name'):
                files.setdefault('extra_data', {}).update(file_info.get('extra_data', {}))
                return result
        result['__instance__']['files'].append(file_info)
        return result
