# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.parsers.__init__ \
    import SoftwareFactsParser


class Parser(SoftwareFactsParser):

    def validate_input(self, source, config):
        pass

    def parse(self, source, config=None, path_prefix=''):
        env = {}
        envvars = source.strip().split("\x00")
        for var in envvars:
            var.strip()
            if var != '':
                key, _, value = var.partition('=')
                env[key] = value
        return env
