from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.del_instance_fact \
    import DelInstanceFact


def test_get_args_spec():
    assert DelInstanceFact.get_args_spec() == {
        'keys': {
            'type': 'list',
            'required': True
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        (['key1', 'key2'], True),
        (dict(keys=['test']), False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = DelInstanceFact(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'del_instance_fact'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    args = [
        'key1',
        'key2.inner1',
        'non_existing',
        'non_existing.key1'
        'key2.non_existing'
    ]
    sw_instance = {
        'key1': 'value1',
        'key2': {
            'inner1': 'inner_value1',
            'inner2': 'inner_value2'
        }
    }
    expected_result = {
        'deleted_from_instance': [
            'key1',
            'key2.inner1'
        ]
    }
    expected_instance = {
        'key2': {
            'inner2': 'inner_value2'
        }
    }
    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = DelInstanceFact(_action_module, {})

    result = plugin.run(args, None, sw_instance)

    assert result == expected_result
    assert sw_instance == expected_instance


def test_run_string(action_module):
    args = 'key1'
    sw_instance = {
        'key1': 'value1',
        'key2': {
            'inner1': 'inner_value1',
            'inner2': 'inner_value2'
        }
    }
    expected_result = {
        'key2': {
            'inner1': 'inner_value1',
            'inner2': 'inner_value2'
        }
    }
    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = DelInstanceFact(_action_module, {})

    plugin.run(args, None, sw_instance)

    assert sw_instance == expected_result


def test_run_no_args(action_module):
    args = []
    sw_instance = {
        'key1': 'value1',
        'key2': {
            'inner1': 'inner_value1',
            'inner2': 'inner_value2'
        }
    }
    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = DelInstanceFact(_action_module, {})

    with pytest.raises(AnsibleRuntimeError) as exinfo:
        plugin.run(args, None, sw_instance)

    assert exinfo.value.message == 'No keys provided, at least one is required for this action to succeed'
