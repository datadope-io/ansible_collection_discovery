from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.add_endpoint_info \
    import AddEndpointInfo


def test_get_args_spec():
    assert AddEndpointInfo.get_args_spec() == {
        'uri': {
            'type': 'str',
            'required': True
        },
        'type': {
            'type': 'str',
            'required': False,
            'default': 'generic'
        },
        'extra_data': {
            'type': 'dict',
            'required': False
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    ((dict(uri='/etc/test/test.conf'), True),
     (dict(type='binary', default='generic'), False),
     (dict(extra_data=dict(test=True)), False))
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = AddEndpointInfo(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'add_endpoint_info'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    args = {
        'uri': '127.0.0.1:8080',
        'type': 'generic',
        'extra_data': {'test': True}
    }
    expected_result = {
        '__instance__': {
            'endpoints': [
                {
                    'uri': '127.0.0.1:8080',
                    'type': 'generic',
                    'extra_data': {'test': True}
                }
            ]
        },
        '__list_merge__': 'append'
    }
    _action_module = action_module(ActionModule)
    plugin = AddEndpointInfo(_action_module, {})
    result = plugin.run(args, None, {})
    assert result == expected_result


def test_run_duplicated(action_module):
    args = {
        'uri': '127.0.0.1:8080',
        'type': 'generic',
        'extra_data': {'test': True}
    }
    sw_instance = {
        'endpoints': [
            {
                'uri': '127.0.0.1:8080',
                'type': 'generic',
                'extra_data': {'test': True}
            }
        ]
    }
    expected_result = {
        '__instance__': {
            'endpoints': [
            ]
        },
        '__list_merge__': 'append'
    }
    _action_module = action_module(ActionModule)
    plugin = AddEndpointInfo(_action_module, {})
    result = plugin.run(args, None, sw_instance)
    assert result == expected_result
