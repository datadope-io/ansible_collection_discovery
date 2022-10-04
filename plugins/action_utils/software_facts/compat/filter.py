# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os  # noqa
from functools import partial  # noqa

from ansible.module_utils.six import string_types, text_type  # noqa

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.__init__ import \
    AnsibleFilterError  # noqa
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.__init__ import \
    is_sequence  # noqa
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.__init__ import \
    unicode_wrap  # noqa


def path_join(paths):
    """ takes a sequence or a string, and return a concatenation
        of the different members """
    if isinstance(paths, string_types):
        return os.path.join(paths)
    elif is_sequence(paths):
        return os.path.join(*paths)
    else:
        raise AnsibleFilterError("| path_join expects string or sequence, got %s instead." % type(paths))


filter_definitions = {
    'path_join': path_join,
    'split': partial(unicode_wrap, text_type.split)
}
