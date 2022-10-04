# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
software_facts_plugin: add_version_info
short_description: Adds version info to the versions list.
description:
     - Manages storing information about a new discovered version into the version list present in the instance.
options:
  version_type:
    description:
      - Information about the origin of the version or the procedure to acquire it.
    type: str
    required: true
    values:
      - active
      - file
      - package
      - docker
      - path
      - add new options if needed
  version_number:
    description:
      - The number of the version as string
    type: str
    required: true
'''

EXAMPLES = r'''
- name: Add version from package
  add_version_info:
    version_type: package
    version_number: 2.0.3
'''


from ansible.utils.display import Display  # noqa

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.__init__ \
    import SoftwareFactsPlugin  # noqa

display = Display()


class AddVersionInfo(SoftwareFactsPlugin):

    def __init__(self, action_module, task_vars):
        super(AddVersionInfo, self).__init__(action_module, task_vars)

    @classmethod
    def get_args_spec(cls):
        return dict(version_type=dict(type='str', required=True),
                    version_number=dict(type='str', required=True))

    def run(self, args=None, attributes=None, software_instance=None):
        version_index = []
        if software_instance:
            version_index = ["{0}_{1}".format(_version['type'], _version['number'])
                             for _version in software_instance.get('version', [])]

        result = dict(__instance__={'version': []}, __list_merge__='append')
        if '{0}_{1}'.format(args['version_type'], args['version_number']) not in version_index:
            result['__instance__']['version'].append(dict(type=args['version_type'],
                                                          number=args['version_number']))
        return result
