from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.add_binding_info \
    import AddBindingInfo


def test_get_args_spec():
    assert AddBindingInfo.get_args_spec() == {
        'address': {
            'type': 'str',
            'required': False
        },
        'port': {
            'type': 'int',
            'required': False
        },
        'class': {
            'type': 'str',
            'required': False,
            'default': 'service'
        },
        'extra_data': {
            'type': 'dict',
            'required': False
        },
        'protocol': {
            'type': 'str',
            'required': False
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        ({'address': '0.0.0.0', 'port': 8080, 'class': 'class_test', 'extra_data': {'test': True}}, True),
        (dict(address='0.0.0.0'), True),
        (dict(port=8080), True),
        (dict(port='1.0.0'), False),
        ({'class': 'class_test'}, False),
        (dict(extra_data=dict(test=True)), False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = AddBindingInfo(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'add_binding_info'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    args = {
        'address': '0.0.0.0',
        'port': 8080,
        'class': 'class_test',
        'extra_data': {'test': True}
    }
    expected_result = {
        '__instance__': {
            'bindings': [
                {
                    'address': '0.0.0.0',
                    'port': 8080,
                    'class': 'class_test',
                    'extra_data': {'test': True}
                }
            ]
        },
        '__list_merge__': 'append'
    }
    _action_module = action_module(ActionModule)
    plugin = AddBindingInfo(_action_module, {})
    result = plugin.run(args, None, {})
    assert result == expected_result


def test_run_duplicated(action_module):
    args = {
        'address': '0.0.0.0',
        'port': 8080
    }
    sw_instance = {
        'bindings': [
            {
                'address': '0.0.0.0',
                'port': 8080
            }
        ]
    }
    expected_result = {
        '__instance__': {
            'bindings': [
            ]
        },
        '__list_merge__': 'append'
    }

    _action_module = action_module(ActionModule)
    plugin = AddBindingInfo(_action_module, {})
    result = plugin.run(args, None, sw_instance)
    assert result == expected_result
