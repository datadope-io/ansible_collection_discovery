from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import patch
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin\
    .which import Which as PluginToTest


def test_get_args_spec():
    assert PluginToTest.get_args_spec() == dict(
        name=dict(type='str', required=True),
        paths=dict(type='list', elements='path', required=True),
        hidden=dict(type='bool', required=False, default=False),
        in_docker=dict(type='bool', required=False, default=True),
        windows_valid_extensions=dict(type='list', elements='str', required=False)
    )


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        (dict(name='value1', paths=['value2']), True),
        (dict(name='value1'), False),
        (dict(paths=['value2']), False),
        (dict(name='value1', paths=['value2'], in_docker=False), True),
        (dict(name='value1', paths=['value2'], in_docker=False, other='anything'), False),
        (dict(name='value1', paths=['value2'], windows_valid_extensions=[".exe", ".ps1"]), True),
        (dict(name='value1', paths=['value2'], windows_valid_extensions=".exe,.ps1"), True)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin"
                                               " 'which'")
    else:
        plugin.validate_args(args)


@pytest.mark.parametrize(
    ('module_result', 'expected_result'),
    (
        (
            dict(failed=False, matched=1,
                 files=[dict(path='the_file_path', isdir=False, xusr=True, xgrp=True, xoth=True)]),
            dict(failed=False, file=dict(path='the_file_path', isdir=False, xusr=True, xgrp=True, xoth=True))
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
            dict(failed=False, matched=0),
            dict(failed=True, msg="No file found with name 'file_name' in '['path1', 'path2']'")
        ),
        (
            dict(failed=False, matched=1,
                 files=[dict(path='the_file_path', isdir=True, xusr=True, xgrp=True, xoth=True)]),
            dict(failed=True, msg="No file found with right attributes for name 'file_name' in '[path1, path2]'")
        ),
        (
            dict(failed=False, matched=1,
                 files=[dict(path='the_file_path', isdir=False, xusr=False, xgrp=False, xoth=False)]),
            dict(failed=True,
                 msg="No file found with right attributes for name 'file_name' in '[path1, path2]'")
        ),
        (
            dict(failed=False, matched=1,
                 files=[dict(path='the_file_path', isdir=False, xusr=False, xgrp=False, xoth=True)]),
            dict(failed=False, file=dict(path='the_file_path', isdir=False, xusr=False, xgrp=False, xoth=True))
        ),
        (
            dict(failed=False, matched=1,
                 files=[dict(path='the_file_path', isdir=False, xusr=False, xgrp=True, xoth=False)]),
            dict(failed=False, file=dict(path='the_file_path', isdir=False, xusr=False, xgrp=True, xoth=False))
        ),
        (
            dict(failed=False, matched=1,
                 files=[dict(path='the_file_path', isdir=False, xusr=True, xgrp=False, xoth=False)]),
            dict(failed=False, file=dict(path='the_file_path', isdir=False, xusr=True, xgrp=False, xoth=False))
        )
    )
)
def test_run(action_module, module_result, expected_result):
    args = dict(name="file_name", paths=['path1', 'path2'], hidden=False, in_docker=True, windows_valid_extensions=None)
    sw_instance = {}

    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, {})

    with patch.object(plugin, '_execute_module') as mocked_execute_module:
        mocked_execute_module.return_value = module_result
        result = plugin.run(args, None, sw_instance)

    module_args = dict(patterns=args['name'], paths=args['paths'], recurse=False, use_regex=False,
                       file_type='file', hidden=args.get('hidden', False))
    mocked_execute_module.assert_called_once_with(
        module_name='ansible.builtin.find',
        module_args=module_args,
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == expected_result


def test_run_in_docker(action_module):
    module_result = dict(failed=False, matched=1,
                         files=[dict(path='/proc/1234/root/path1/file_name',
                                     isdir=False, xusr=True, xgrp=True, xoth=True)])
    expected_result = dict(failed=False, file=dict(path='/path1/file_name', isdir=False, xusr=True, xgrp=True,
                                                   xoth=True))
    args = dict(name="file_name", paths=['/path1', '/path2'], hidden=False, in_docker=True,
                windows_valid_extensions=None)
    sw_instance = {"docker": {"name": "docker-name"},
                   "process": {"pid": "1234"}}

    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, sw_instance)

    with patch.object(plugin, '_execute_module') as mocked_execute_module:
        mocked_execute_module.return_value = module_result
        result = plugin.run(args, None, sw_instance)

    module_args = dict(patterns=args['name'], paths=['/proc/1234/root/path1', '/proc/1234/root/path2'],
                       recurse=False, use_regex=False,
                       file_type='file', hidden=args.get('hidden', False))
    mocked_execute_module.assert_called_once_with(
        module_name='ansible.builtin.find',
        module_args=module_args,
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == expected_result


def test_run_not_in_docker_having_docker(action_module):
    module_result = dict(failed=False, matched=1,
                         files=[dict(path='/path1/file_name',
                                     isdir=False, xusr=True, xgrp=True, xoth=True)])
    expected_result = dict(failed=False, file=dict(path='/path1/file_name', isdir=False, xusr=True, xgrp=True,
                                                   xoth=True))
    args = dict(name="file_name", paths=['/path1', '/path2'], hidden=False, in_docker=False,
                windows_valid_extensions=None)
    sw_instance = {"docker": {"name": "docker-name"},
                   "process": {"pid": "1234"}}

    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, sw_instance)

    with patch.object(plugin, '_execute_module') as mocked_execute_module:
        mocked_execute_module.return_value = module_result
        result = plugin.run(args, None, sw_instance)

    module_args = dict(patterns=args['name'], paths=['/path1', '/path2'],
                       recurse=False, use_regex=False,
                       file_type='file', hidden=args.get('hidden', False))
    mocked_execute_module.assert_called_once_with(
        module_name='ansible.builtin.find',
        module_args=module_args,
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == expected_result


def test_run_in_windows(action_module):
    module_result = dict(failed=False, matched=1,
                         files=[dict(path='\\path1\\file_name.ps1',
                                     isdir=False, extension=".ps1")])
    expected_result = dict(failed=False, file=dict(path='\\path1\\file_name.ps1', isdir=False, extension=".ps1"))
    args = dict(name="file_name.ps1", paths=['\\path1', '\\path2'], hidden=False, in_docker=False,
                windows_valid_extensions=None)
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

    module_args = dict(patterns=args['name'], paths=args['paths'],
                       recurse=False, use_regex=False,
                       file_type='file', hidden=args.get('hidden', False))
    mocked_execute_module.assert_called_once_with(
        module_name='ansible.windows.win_find',
        module_args=module_args,
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == expected_result


def test_run_in_windows_invalid_ext(action_module):
    module_result = dict(failed=False, matched=1,
                         files=[dict(path='\\path1\\file_name.ps1',
                                     isdir=False, extension=".ps1")])
    expected_result = dict(
        failed=True, msg="No file found with right attributes for name 'file_name.ps1' in '[\\path1, \\path2]'")
    args = dict(name="file_name.ps1", paths=['\\path1', '\\path2'], hidden=False, in_docker=False,
                windows_valid_extensions=['.exe'])
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

    module_args = dict(patterns=args['name'], paths=args['paths'],
                       recurse=False, use_regex=False,
                       file_type='file', hidden=args.get('hidden', False))
    mocked_execute_module.assert_called_once_with(
        module_name='ansible.windows.win_find',
        module_args=module_args,
        task_vars=plugin._task_vars,
        wrap_async=plugin._task.async_val)
    assert result == expected_result
