from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import patch
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin\
    .stat import Stat as PluginToTest


def test_get_args_spec():
    assert PluginToTest.get_args_spec() == dict(
        path=dict(type='path', required=True, aliases=['dest', 'name']),
        follow=dict(type='bool', default=False),
        get_mime=dict(type='bool', default=True, aliases=['mime', 'mime_type', 'mime-type']),
        get_attributes=dict(type='bool', default=True, aliases=['attr', 'attributes']),
        in_docker=dict(type='bool', required=False, default=True)
    )


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        (dict(path='value1'), True),
        (dict(other='value1'), False),
        (dict(path='value1', in_docker=False), True),
        (dict(name='value1', in_docker=False, other='anything'), False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin"
                                               " 'stat'")
    else:
        plugin.validate_args(args)


@pytest.mark.parametrize(
    ('module_result', 'expected_result'),
    (
        (
            dict(failed=False,
                 stat=dict(exists=True, executable=True, path="/dir/file")),
            dict(failed=False, stat=dict(exists=True, executable=True, path="/dir/file"))
        ),
        (
            dict(failed=True, msg="The error message"),
            dict(failed=True, msg="The error message")
        ),
        (
            dict(failed=True, msg="The error message", exception="The exception"),
            dict(failed=True, msg="The error message", exception="The exception")
        ),
        (
            dict(failed=False, stat=dict(exists=False)),
            dict(failed=True, msg="Path '/dir/file' not found")
        )
    )
)
def test_run(action_module, module_result, expected_result):
    args = dict(path="/dir/file", in_docker=True)
    sw_instance = {}

    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, {})

    with patch.object(plugin, '_execute_module') as mocked_execute_module:
        mocked_execute_module.return_value = module_result
        result = plugin.run(args, None, sw_instance)

    module_args = dict(path="/dir/file", get_checksum=False)
    mocked_execute_module.assert_called_once_with(
        module_name='ansible.builtin.stat',
        module_args=module_args,
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == expected_result


def test_run_in_docker(action_module):
    module_result = dict(failed=False,
                         stat=dict(exists=True, executable=True, path="/proc/1234/root/dir/file"))
    expected_result = dict(failed=False, stat=dict(exists=True, executable=True, path="/dir/file"))
    args = dict(path="/dir/file", in_docker=True)
    sw_instance = {"docker": {"name": "docker-name"},
                   "process": {"pid": "1234"}}

    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, sw_instance)

    with patch.object(plugin, '_execute_module') as mocked_execute_module:
        mocked_execute_module.return_value = module_result
        result = plugin.run(args, None, sw_instance)

    module_args = dict(path="/proc/1234/root/dir/file", get_checksum=False)
    mocked_execute_module.assert_called_once_with(
        module_name='ansible.builtin.stat',
        module_args=module_args,
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == expected_result


def test_run_not_in_docker_having_docker(action_module):
    module_result = dict(failed=False,
                         stat=dict(exists=True, executable=True, path="/dir/file"))
    expected_result = dict(failed=False, stat=dict(exists=True, executable=True, path="/dir/file"))
    args = dict(path="/dir/file", in_docker=False)
    sw_instance = {"docker": {"name": "docker-name"},
                   "process": {"pid": "1234"}}

    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, sw_instance)

    with patch.object(plugin, '_execute_module') as mocked_execute_module:
        mocked_execute_module.return_value = module_result
        result = plugin.run(args, None, sw_instance)

    module_args = dict(path="/dir/file", get_checksum=False)
    mocked_execute_module.assert_called_once_with(
        module_name='ansible.builtin.stat',
        module_args=module_args,
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == expected_result


def test_run_not_in_windows(action_module):
    module_result = dict(failed=False,
                         stat=dict(exists=True, extension=".exe", path="\\dir\\file.exe"))
    expected_result = dict(failed=False, stat=dict(exists=True, extension=".exe", path="\\dir\\file.exe"))
    args = dict(path="\\dir\\file.exe", in_docker=False)
    sw_instance = {}
    task_vars = {
        "ansible_facts": {
            "os_family": "windows"
        }
    }

    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, task_vars)

    with patch.object(plugin, '_execute_module') as mocked_execute_module:
        mocked_execute_module.return_value = module_result
        result = plugin.run(args, None, sw_instance)

    module_args = dict(path="\\dir\\file.exe", get_checksum=False)
    mocked_execute_module.assert_called_once_with(
        module_name='ansible.windows.win_stat',
        module_args=module_args,
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == expected_result
