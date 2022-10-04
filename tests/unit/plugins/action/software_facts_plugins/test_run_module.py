from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import patch
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin\
    .run_module import RunModule


def test_get_args_spec():
    assert RunModule.get_args_spec() == {
        'key_value': {
            'type': 'str',
            'required': True
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        (dict(the_module_name=dict(arg1='value1', arg2='value2')), True),
        (dict(the_module_name=dict(arg1='value1', arg2='value2'), other='other'), False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = RunModule(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin"
                                               " 'run_module'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    module_result = 'The result'

    args = {
        'the_module_name': {
            'arg1': 'val1',
            'arg2': 'val2'
        }
    }
    sw_instance = {}

    _action_module = action_module(ActionModule)
    plugin = RunModule(_action_module, {})

    with patch.object(plugin, '_execute_module') as mocked_execute_module:
        mocked_execute_module.return_value = module_result
        result = plugin.run(args, None, sw_instance)

    mocked_execute_module.assert_called_once_with(
        module_name='the_module_name',
        module_args={'arg1': 'val1', 'arg2': 'val2'},
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == module_result
