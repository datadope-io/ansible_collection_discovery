# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleRuntimeError
from ansible.utils.display import Display

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.parsers.__init__ \
    import SoftwareFactsParser
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.xmltodict import parse

display = Display()


class XMLParser(SoftwareFactsParser):

    def validate_input(self, source, config=None):
        if config is not None and not isinstance(config, dict):
            raise AnsibleRuntimeError("Invalid config provided for the xml parser; config must be a dict when provided")

    def parse(self, source, config=None, path_prefix=''):
        if config is None:
            config = {}

        attr_prefix = config.get('attr_prefix', 'attr-')

        try:
            return parse(source, attr_prefix=attr_prefix)
        except Exception as e:
            raise AnsibleRuntimeError("Cannot parse text into XML: {0}".format(str(e)))
