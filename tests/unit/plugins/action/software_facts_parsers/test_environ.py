from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.parsers.environ import Parser


@pytest.mark.parametrize(
    ('text', 'expected_result'),
    (
        ('env_var1=value1\x00\x00env_var2=value2\n', dict(env_var1='value1', env_var2='value2')),
        ('\n', dict())
    )
)
def test_run(action_module, text, expected_result):
    _action_module = action_module(ActionModule)
    parser = Parser(_action_module, None)
    result = parser.parse(text, None)
    assert result == expected_result
