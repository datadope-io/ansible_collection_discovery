from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import base64

import pytest

from ansible.module_utils.common.text.converters import to_bytes
from ansible.errors import AnsibleRuntimeError
from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import patch
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin\
    .read_environment_for_process import ReadEnvironmentForProcess


def test_get_args_spec():
    assert ReadEnvironmentForProcess.get_args_spec() == {
        'pid': {
            'type': 'str',
            'required': True
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        (dict(pid='1000'), True),
        (dict(pid=1000), True),
        (dict(pid='1000', other='other'), False),
        (dict(other='1000'), False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = ReadEnvironmentForProcess(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin"
                                               " 'read_environment_for_process'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    file_contents = 'env_var1=value1\x00\x00env_var2=value2\n'

    args = {
        'pid': '1000',
    }
    sw_instance = {}

    _action_module = action_module(ActionModule)
    plugin = ReadEnvironmentForProcess(_action_module, {})

    with patch.object(plugin, '_execute_module') as mocked_slurp:
        mocked_slurp.return_value = dict(content=base64.b64encode(to_bytes(file_contents)),
                                         failed=False,
                                         encoding='base64')
        result = plugin.run(args, None, sw_instance)

    mocked_slurp.assert_called_once_with(
        module_name='ansible.legacy.slurp',
        module_args=dict(src='/proc/1000/environ'),
        task_vars={})
    assert result == dict(content=file_contents, failed=False,
                          parsed={'env_var1': 'value1', 'env_var2': 'value2'})
