from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.add_file_info \
    import AddFileInfo


def test_get_args_spec():
    assert AddFileInfo.get_args_spec() == {
        'path': {
            'type': 'str',
            'required': True
        },
        'type': {
            'type': 'str',
            'required': True
        },
        'name': {
            'type': 'str',
            'required': False,
        },
        'subtype': {
            'type': 'str',
            'required': False,
        },
        'extra_data': {
            'type': 'dict',
            'required': False
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    ((dict(path='/etc/test/test.conf', type='binary'), True),
     (dict(type='binary', path='a/b'), True),
     (dict(name='test.conf'), False),
     (dict(subtype='generic'), False),
     (dict(extra_data=dict(test=True)), False))
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = AddFileInfo(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'add_file_info'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    args = {
        'path': '/etc/test/test.conf',
        'type': 'binary',
        'name': 'test.conf',
        'subtype': 'generic',
        'extra_data': {'test': True}
    }
    expected_result = {
        '__instance__': {
            'files': [
                {
                    'path': '/etc/test/test.conf',
                    'type': 'binary',
                    'name': 'test.conf',
                    'subtype': 'generic',
                    'extra_data': {'test': True}
                }
            ]
        },
        '__list_merge__': 'append'
    }
    _action_module = action_module(ActionModule)
    plugin = AddFileInfo(_action_module, {})
    result = plugin.run(args, None, {})
    assert result == expected_result


def test_run_duplicated(action_module):
    args = {
        'path': '/etc/test/test.conf',
        'type': 'binary',
        'name': 'test.conf',
        'subtype': 'generic',
        'extra_data': {'test': True}
    }
    sw_instance = {
        'files': [
            {
                'path': '/etc/test/test.conf',
                'type': 'binary',
                'name': 'test.conf',
                'subtype': 'generic',
                'extra_data': {'test': True}
            }
        ]
    }
    expected_result = {
        '__instance__': {
            'files': [
            ]
        },
        '__list_merge__': 'append'
    }
    _action_module = action_module(ActionModule)
    plugin = AddFileInfo(_action_module, {})
    result = plugin.run(args, None, sw_instance)
    assert result == expected_result
