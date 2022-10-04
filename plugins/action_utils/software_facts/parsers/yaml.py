# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleRuntimeError
from ansible.parsing.utils.yaml import from_yaml
from ansible.utils.display import Display

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.parsers.__init__ \
    import SoftwareFactsParser

display = Display()


class YamlParser(SoftwareFactsParser):

    def validate_input(self, source, config):
        pass

    def parse(self, source, config=None, path_prefix=''):
        if config is None:
            config = {}
        try:
            return from_yaml(source, **config)
        except Exception as e:
            raise AnsibleRuntimeError("Cannot parse text into yaml: {0}".format(str(e)))
