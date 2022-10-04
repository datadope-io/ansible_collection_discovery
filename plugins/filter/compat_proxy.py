# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.filter import filter_definitions


class FilterModule(object):
    def filters(self):  # noqa
        return filter_definitions
