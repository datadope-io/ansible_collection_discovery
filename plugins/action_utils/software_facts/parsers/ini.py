# Copyright: (c) 2023, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import configparser

from ansible.errors import AnsibleRuntimeError
from ansible.utils.display import Display

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.parsers.__init__ \
    import SoftwareFactsParser

display = Display()


class IniParser(SoftwareFactsParser):

    def validate_input(self, source, config):
        pass

    def parse(self, source, config=None, path_prefix=''):
        ini = configparser.ConfigParser()

        if config is None:
            config = {}

        try:
            try:
                ini.read_string(source, **config)
            except configparser.MissingSectionHeaderError:
                # If the .ini file doesn't have a section header, add a default section header.
                # https://stackoverflow.com/a/70134461/1407722
                ini.read_string('[default]\n' + source, **config)

            return {s: dict(ini.items(s)) for s in ini.sections()}
        except Exception as e:
            raise AnsibleRuntimeError("Cannot parse text into ini: {0}".format(str(e)))
