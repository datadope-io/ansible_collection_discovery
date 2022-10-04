from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.set_instance_fact \
    import SetInstanceFact


def test_get_args_spec():
    assert SetInstanceFact.get_args_spec() == {
        'key_value': {
            'type': 'dict',
            'required': True
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        ({'key1': 'value1', 'key2': 'value2'}, True),
        (['l1', 'l2'], False),
        ('text', False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = SetInstanceFact(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin"
                                               " 'set_instance_fact'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    args = {
        'key1': 'value1',
        'key2': 'yes'
    }
    expected_result = {
        '__instance__': {
            'key1': 'value1',
            'key2': True
        }
    }
    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = SetInstanceFact(_action_module, {})

    result = plugin.run(args, None, None)

    assert result == expected_result


def test_run_no_args(action_module):
    args = {}
    sw_instance = {
        'key1': 'value1',
        'key2': {
            'inner1': 'inner_value1',
            'inner2': 'inner_value2'
        }
    }
    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = SetInstanceFact(_action_module, {})

    with pytest.raises(AnsibleRuntimeError) as exinfo:
        plugin.run(args, None, sw_instance)

    assert exinfo.value.message == 'No key/value pairs provided, at least one is required for this action to succeed'


def test_run_bad_name(action_module):
    args = {
        11: 'value1',
        'key2': 'value2'
    }
    sw_instance = {
        'existing2': 'value1',
        'key2': {
            'inner1': 'inner_value1',
            'inner2': 'inner_value2'
        }
    }
    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = SetInstanceFact(_action_module, {})

    with pytest.raises(AnsibleRuntimeError) as exinfo:
        plugin.run(args, None, sw_instance)

    assert exinfo.value.message == "The variable name '11' is not valid. " \
                                   "Variables must start with a letter or underscore character, " \
                                   "and contain only letters, numbers and underscores."
