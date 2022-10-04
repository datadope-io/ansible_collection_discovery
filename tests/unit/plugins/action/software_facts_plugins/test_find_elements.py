from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.find_elements \
    import FindElements as PluginToTest


def test_get_args_spec():
    assert PluginToTest.get_args_spec() == {
        'source': {
            'type': 'list',
            'required': True
        },
        'filter': {
            'type': 'dict',
            'required': False,
            'default': {}
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        (dict(source=[{'foo': 1, 'bar': False}], filter={'foobar': False}), True),
        (dict(source=[{'foo': 1, 'bar': False}]), True),
        (dict(filter='fail'), False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'find_elements'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    args = {
        'source': [
            {
                'name': 'element_1',
                'value': 1
            },
            {
                'name': 'element_2',
                'value': 1
            },
            {
                'name': 'element_3',
                'value': 2
            }
        ],
        'filter': {
            'value': 1
        }
    }
    expected_result = [
        {
            'name': 'element_1',
            'value': 1
        },
        {
            'name': 'element_2',
            'value': 1
        }
    ]

    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = PluginToTest(_action_module, {})

    result = plugin.run(args, None, None)

    assert result == expected_result


def test_run_no_filter(action_module):
    args = {
        'source': [
            {
                'name': 'element_1',
                'value': 1
            },
            {
                'name': 'element_2',
                'value': 1
            },
            {
                'name': 'element_3',
                'value': 2
            }
        ],
        'filter': {}
    }
    expected_result = [
        {
            'name': 'element_1',
            'value': 1
        },
        {
            'name': 'element_2',
            'value': 1
        },
        {
            'name': 'element_3',
            'value': 2
        }
    ]

    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = PluginToTest(_action_module, {})

    result = plugin.run(args, None, None)

    assert result == expected_result


def test_run_nested(action_module):
    args = {
        'source': [
            {
                'name': 'element_1',
                'value': 1,
                'nested': {
                    'nested_1': 1,
                    'nested_2': 2
                }
            },
            {
                'name': 'element_2',
                'value': 1,
                'nested': {
                    'nested_2': 2,
                    'nested_3': 3
                }
            },
            {
                'name': 'element_3',
                'value': 2,
                'nested': {
                    'nested_1': 1,
                    'nested_4': 4
                }
            }
        ],
        'filter': {
            'nested': {
                'nested_2': 2
            }
        }
    }
    expected_result = [
        {
            'name': 'element_1',
            'value': 1,
            'nested': {
                'nested_1': 1,
                'nested_2': 2
            }
        },
        {
            'name': 'element_2',
            'value': 1,
            'nested': {
                'nested_2': 2,
                'nested_3': 3
            }
        }
    ]

    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = PluginToTest(_action_module, {})

    result = plugin.run(args, None, None)

    assert result == expected_result
