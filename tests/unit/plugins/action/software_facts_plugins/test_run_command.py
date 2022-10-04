from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import patch
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin\
    .run_command import RunCommand as PluginToTest


def test_get_args_spec():
    assert PluginToTest.get_args_spec() == dict(
        cmd=dict(type='str', required=False),
        argv=dict(type='list', required=False),
        in_docker=dict(type='bool', required=False, default=True)
    )


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        (dict(cmd='value1'), True),
        (dict(argv=['value2']), True),
        (dict(cmd='value1', argv=['value2']), False),
        (dict(cmd='value1', other=['value2']), True),
        (dict(argv=['value2'], other=['value2']), True),
        (dict(arg1='value1', arg2='value2', other='other'), False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin"
                                               " 'run_command'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    module_result = 'The result'

    args = dict(cmd="command line", in_docker=True)
    sw_instance = {}

    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, {})

    with patch.object(plugin, '_execute_module') as mocked_execute_module:
        mocked_execute_module.return_value = module_result
        result = plugin.run(args, None, sw_instance)

    mocked_execute_module.assert_called_once_with(
        module_name='command',
        module_args={'_raw_params': "command line"},
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == module_result


def test_run_in_docker(action_module):
    module_result = 'The result'

    args = dict(cmd="command line", in_docker=True)
    sw_instance = {"docker": {"name": "docker-name"},
                   "process": {"pid": "1234"}}

    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, sw_instance)

    with patch.object(plugin, '_execute_module') as mocked_execute_module:
        mocked_execute_module.return_value = module_result
        result = plugin.run(args, None, sw_instance)

    mocked_execute_module.assert_called_once_with(
        module_name='command',
        module_args={'_raw_params': "nsenter -t 1234 -m -u -n -p command line"},
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == module_result


def test_run_in_docker_argv(action_module):
    module_result = 'The result'

    args = dict(argv=["command", "line"], in_docker=True)
    sw_instance = {"docker": {"name": "docker-name"},
                   "process": {"pid": "1234"}}

    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, sw_instance)

    with patch.object(plugin, '_execute_module') as mocked_execute_module:
        mocked_execute_module.return_value = module_result
        result = plugin.run(args, None, sw_instance)

    mocked_execute_module.assert_called_once_with(
        module_name='command',
        module_args={'argv': ["nsenter", "-t", "1234", "-m", "-u", "-n", "-p", "command", "line"]},
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == module_result


def test_run_not_in_docker_having_docker(action_module):
    module_result = 'The result'

    args = dict(cmd="command line", in_docker=False)
    sw_instance = {"docker": {"name": "docker-name"},
                   "process": {"pid": "1234"}}

    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, sw_instance)

    with patch.object(plugin, '_execute_module') as mocked_execute_module:
        mocked_execute_module.return_value = module_result
        result = plugin.run(args, None, sw_instance)

    mocked_execute_module.assert_called_once_with(
        module_name='command',
        module_args={'_raw_params': "command line"},
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == module_result
