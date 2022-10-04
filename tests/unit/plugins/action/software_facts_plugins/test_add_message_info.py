from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.add_message_info \
    import AddMessageInfo


def test_get_args_spec():
    assert AddMessageInfo.get_args_spec() == {
        'msg': {
            'type': 'str',
            'required': True
        },
        'key': {
            'type': 'str',
            'required': False
        },
        'value': {
            'type': 'raw',
            'required': False
        },
        'extra_data': {
            'type': 'dict',
            'required': False
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    ((dict(msg='Test message from server'), True),
     (dict(key='test_connect'), False),
     (dict(vaue=True), False),
     (dict(extra_data=dict(test=True)), False))
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = AddMessageInfo(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'add_message_info'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    args = {
        'msg': 'Test message from server',
        'key': 'test_connect',
        'value': True,
        'extra_data': {'test': True}
    }
    expected_result = {
        '__instance__': {
            'messages': [
                {
                    'msg': 'Test message from server',
                    'key': 'test_connect',
                    'value': True,
                    'extra_data': {'test': True}
                }
            ]
        },
        '__list_merge__': 'append'
    }
    _action_module = action_module(ActionModule)
    plugin = AddMessageInfo(_action_module, {})
    result = plugin.run(args, None, {})
    assert result == expected_result


def test_run_duplicated(action_module):
    args = {
        'msg': 'Test message from server',
        'key': 'test_connect',
        'value': True,
        'extra_data': {'test': True}
    }
    sw_instance = {
        'messages': [
            {
                'msg': 'Test message from server',
                'key': 'test_connect',
                'value': True,
                'extra_data': {'test': True}
            }
        ]
    }
    expected_result = {
        '__instance__': {
            'messages': [
            ]
        },
        '__list_merge__': 'append'
    }

    _action_module = action_module(ActionModule)
    plugin = AddMessageInfo(_action_module, {})
    result = plugin.run(args, None, sw_instance)
    assert result == expected_result
