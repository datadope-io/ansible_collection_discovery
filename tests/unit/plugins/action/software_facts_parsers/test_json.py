from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.parsers.json import JsonParser


@pytest.mark.parametrize(
    ('text', 'expected_result'),
    (
        ('{"key": "value"}', dict(key='value')),
        ('["elem1", "elem2"]', ["elem1", "elem2"])
    )
)
def test_run(action_module, text, expected_result):
    _action_module = action_module(ActionModule)
    parser = JsonParser(_action_module, None)
    result = parser.parse(text, None)
    assert result == expected_result


@pytest.mark.parametrize(
    ('text', 'expected_exception_message_beginning'),
    (
        ('{"key": "value"', "Cannot parse text into json: "),
        ('a text', "Cannot parse text into json: ")
    )
)
def test_run_error(action_module, text, expected_exception_message_beginning):
    _action_module = action_module(ActionModule)
    parser = JsonParser(_action_module, None)
    with pytest.raises(AnsibleRuntimeError) as exc_info:
        parser.parse(text, {})
    assert exc_info.value.message.startswith(expected_exception_message_beginning)
