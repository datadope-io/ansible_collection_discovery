from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.parsers.key_value import Parser


@pytest.mark.parametrize(
    ('text', 'expected_result'),
    (
        ("""
        key1=value1
        # commented line
        ; other commented line
        // third commented line
        key2 value2  # comment end of line
        key3=value3 with spaces and=in the value # other comment end of line
        key4 value4 with spaces in the value
        key5=
        """, dict(key1='value1',
                  key2='value2',
                  key3='value3 with spaces and=in the value',
                  key4='value4 with spaces in the value',
                  key5='')),
    )
)
def test_run(action_module, text, expected_result):
    _action_module = action_module(ActionModule)
    parser = Parser(_action_module, None)
    result = parser.parse(text, dict(separators='= ', comment_delimiters=['#', ';', '//']))
    assert result == expected_result


@pytest.mark.parametrize(
    ('text', 'expected_result'),
    (
        ("""
        key1=value1
        # commented line
        ; other commented line
        key2 value2  # comment end of line
        key3=value3 with spaces and=in the value # other comment end of line
        key4 value4 with spaces in the value
        key5=
        """, dict(key1='value1',
                  key2='value2',
                  key3='value3 with spaces and=in the value',
                  key4='value4 with spaces in the value',
                  key5='')),
    )
)
def test_run_other_parameter_type(action_module, text, expected_result):
    _action_module = action_module(ActionModule)
    parser = Parser(_action_module, None)
    result = parser.parse(text, dict(separators=['=', ' '], comment_delimiters='#;'))
    assert result == expected_result


@pytest.mark.parametrize(
    ('text', 'expected_result'),
    (
        ("""
        key1=value1
        # commented line
        ; other commented line
        key3=value3 with spaces and=in the value # other comment end of line
        key5=
        """, dict(key1='value1',
                  key3='value3 with spaces and=in the value',
                  key5='')),
    )
)
def test_run_other_no_parameters(action_module, text, expected_result):
    _action_module = action_module(ActionModule)
    parser = Parser(_action_module, None)
    result = parser.parse(text, None)
    assert result == expected_result
