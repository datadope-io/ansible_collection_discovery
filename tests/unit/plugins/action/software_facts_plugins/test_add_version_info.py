from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.add_version_info \
    import AddVersionInfo


def test_get_args_spec():
    assert AddVersionInfo.get_args_spec() == {
        'version_type': {
            'type': 'str',
            'required': True
        },
        'version_number': {
            'type': 'str',
            'required': True
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        (dict(version_type='test', version_number='1.0.0'), True),
        (dict(version_type='test'), False),
        (dict(version_number='1.0.0'), False),
        (dict(version_number=1), False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = AddVersionInfo(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'add_version_info'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    args = {
        'version_type': 'the version type',
        'version_number': 'the version number'
    }
    expected_result = {
        '__instance__': {
            'version': [
                {
                    'type': 'the version type',
                    'number': 'the version number'
                }
            ]
        },
        '__list_merge__': 'append'
    }
    _action_module = action_module(ActionModule)
    plugin = AddVersionInfo(_action_module, {})

    result = plugin.run(args, None, None)

    assert result == expected_result
