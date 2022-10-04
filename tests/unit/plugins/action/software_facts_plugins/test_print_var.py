from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json

import pytest

from ansible import constants as C  # noqa
from ansible.errors import AnsibleRuntimeError, AnsibleUndefinedVariable
from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import patch
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.print_var \
    import PrintVar


def test_get_args_spec():
    assert PrintVar.get_args_spec() == {
        'var': {
            'type': 'str',
            'required': True
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        (dict(var='test'), True),
        (dict(var=1), True),
        (dict(other='value'), False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = PrintVar(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'print_var'")
    else:
        plugin.validate_args(args)


@pytest.mark.parametrize(
    ('var', 'task_vars', 'result_value'),
    (
        ('key1', {'key1': 'value1', 'inventory_hostname': 'the_host'}, 'value1'),
        ('{{ key1 }}', {'key1': 'value1', 'inventory_hostname': 'the_host'}, 'value1'),
        ('key1', {'key1': {'inner1': 'value1'}, 'inventory_hostname': 'the_host'}, json.dumps({"inner1": "value1"},
                                                                                              indent=4)),
        ('key1', {'key1': ['inner1', 'inner2'], 'inventory_hostname': 'the_host'}, json.dumps(["inner1", "inner2"],
                                                                                              indent=4))
    )
)
def test_run(action_module, var, task_vars, result_value):

    def mocked_template(var, **kwargs):  # noqa
        if '{{' not in var:
            return var
        return task_vars[var.replace('{{', '').replace('}}', '').strip()]

    args = {
        'var': var
    }
    sw_instance = {}
    _action_module = action_module(ActionModule)
    _action_module._templar.template = mocked_template
    plugin = PrintVar(_action_module, task_vars)
    with patch('ansible_collections.datadope.discovery.plugins.action_utils'
               '.software_facts.plugins.builtin.print_var.display') as mocked_display:
        plugin.run(args, None, sw_instance)

    mocked_display.display.assert_called_once_with('<the_host> {0} = {1}'.format(var, result_value), color='green')


@pytest.mark.parametrize(
    ('verbosity', 'result_string'),
    (
        (0, u'VARIABLE IS NOT DEFINED!'),
        (1, u'VARIABLE IS NOT DEFINED!: key1')
    )
)
def test_run_undefined(action_module, verbosity, result_string):
    task_vars = {'inventory_hostname': 'the_host'}

    def mocked_template(var, **kwargs):  # noqa
        if '{{' in var:
            return var
        if var not in task_vars:
            raise AnsibleUndefinedVariable(var)
        return task_vars[var.replace('{{', '').replace('}}', '')]

    args = {
        'var': 'key1'
    }
    sw_instance = {}
    _action_module = action_module(ActionModule)
    _action_module._templar.template = mocked_template
    plugin = PrintVar(_action_module, task_vars)
    with patch('ansible_collections.datadope.discovery.plugins.action_utils'
               '.software_facts.plugins.builtin.print_var.display') as mocked_display:
        plugin._display = mocked_display
        mocked_display.verbosity = verbosity
        plugin.run(args, None, sw_instance)

    mocked_display.display.assert_called_once_with('<the_host> key1 = {0}'.format(result_string), color='green')
