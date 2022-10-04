import os
import time

import pytest

from ansible.errors import AnsibleRuntimeError
from ansible.module_utils.six import iteritems
from ansible.template import Templar
from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import patch
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins import SoftwareFactsPlugin


class DoNothingPlugin(SoftwareFactsPlugin):
    filters = None

    def __init__(self, action_module, task_vars):
        super(DoNothingPlugin, self).__init__(action_module, task_vars)

    @classmethod
    def get_args_spec(cls):
        return {}

    def validate_args(self, args):
        return args

    def run(self, args=None, attributes=None, software_instance=None):
        return dict(parameters=args)


@pytest.mark.parametrize(argnames=['data_file_path'],
                         argvalues=pytest.file_list)
def test_auto_software_facts(read_file, normalize, data_file_path):
    data = read_file(data_file_path)
    expected_result = data.pop('expected_result')
    ansible_facts_given = data.get('task_vars', {}).pop('ansible_facts', {})
    ansible_facts = {
        "processes": data.get("processes", []),
        "packages": data.get("packages", {}),
        "tcp_listen": data.get("tcp_listen", []),
        "udp_listen": data.get("udp_listen", [])
    }
    ansible_facts.update(ansible_facts_given)
    task_vars = {
        'inventory_hostname': 'target_host',
        'ansible_hostname': 'target_host',
        'ansible_facts': ansible_facts,
        'dockers': data.get("dockers"),  # Not present in ansible_facts, don't know why
    }
    task_vars.update(ansible_facts)  # Vars are provided as ansible_facts and as first level var
    task_vars.update(data.pop('task_vars', {}))  # Add vars from test definition file
    mocked_plugin_tasks = data.pop('mocked_plugin_tasks', {})
    expected_tasks_calls = data.pop('expected_tasks_calls', None)
    expected_tasks_calls_strict = data.pop('expected_tasks_calls_mode_strict', False)
    tasks_calls = dict()

    original_get_software_facts_plugin = ActionModule.get_software_facts_plugin

    class MockedPlugin(SoftwareFactsPlugin):

        def __init__(self, original, task, action, _task_vars):
            super(MockedPlugin, self).__init__(action, _task_vars)
            self._original = original
            self._task = task

        def validate_args(self, args):
            return self._original.validate_args(args)

        @classmethod
        def get_args_spec(cls):
            return {}

        def run(self, args=None, attributes=None, software_instance=None):
            call_number = tasks_calls[self._task]
            mocking_info = mocked_plugin_tasks.get(self._task, {})
            calls_info = mocking_info.get('calls')
            if calls_info is not None:
                assert len(calls_info) >= call_number, \
                    "Task '{0}' should not be called more than {1} times".format(self._task, len(calls_info))
                call_info = calls_info[call_number - 1]
                if isinstance(call_info, str) and call_info == 'run':
                    call_info = {}
            else:
                call_info = mocking_info
            if 'expected_args' in call_info:
                if args is None:
                    assert not call_info['expected_args']
                assert normalize(args) == normalize(call_info['expected_args']), \
                    "Task '{0}' call number {2} called with unexpected arguments: {1}".format(self._task,
                                                                                              args,
                                                                                              call_number)
            if 'expected_attributes' in call_info:
                if attributes is None:
                    assert not call_info['expected_attributes']
                assert normalize(attributes) == normalize(call_info['expected_attributes']), \
                    "Task '{0}'  call number {2} called with unexpected attributes: {1}".format(self._task,
                                                                                                attributes,
                                                                                                call_number)
            if 'fail' in call_info:
                assert False, call_info['fail']
            if 'sleep' in call_info:
                time.sleep(float(call_info['sleep']))
            if 'raise_exception' in call_info:
                raise(AnsibleRuntimeError(message=call_info['raise_exception']))
            if 'plugin_result' in call_info:
                return call_info['plugin_result']
            if 'execute_module_result' in call_info:
                #  Invoke original plugin patching execute_module
                with patch.object(self._original, '_execute_module',
                                  return_value=call_info['execute_module_result'].copy()):
                    original_result = self._original.run(args, attributes, software_instance)
            else:
                #  Invoke original plugin
                original_result = self._original.run(args, attributes, software_instance)
            if 'expected_result' in call_info:
                assert normalize(original_result) == normalize(call_info['expected_result']), \
                    "Wrong result for task '{0}'".format(self._task)
            return original_result

    def mocked_get_software_facts_plugin(cls, name, action, _task_vars, task):  # noqa
        if name == 'testing_plugin':
            return DoNothingPlugin(action, _task_vars)
        try:
            if name in ('block', 'include_tasks'):
                plugin = name
            else:
                plugin = original_get_software_facts_plugin(name, action, _task_vars)
            return MockedPlugin(plugin, task, action, _task_vars)
        except AnsibleRuntimeError:
            assert False, "Plugin '{0}' not found".format(name)

    if 'software_discovery__custom_tasks_definition_files_path' not in task_vars:
        task_vars['software_discovery__custom_tasks_definition_files_path'] = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '../../../../../roles/software_discovery/files/tasks_definitions'))

    _templar = Templar(None)
    _templar.available_variables = task_vars
    action_module = ActionModule(task=None, connection=None, play_context=None, loader=None, shared_loader_obj=None,
                                 templar=_templar)

    original_execute_plugin_for_item = action_module._execute_plugin_for_item
    original_execute_plugin_for_item_async = action_module._execute_plugin_for_item_async

    def mocked_execute_plugin_for_item(args, attributes, desc, in_block, item, item_result_holder, name,
                                       plugin, software_instance, _task_vars, index):
        tasks_calls[desc] = tasks_calls.setdefault(desc, 0) + 1
        call_info = {}
        if desc in mocked_plugin_tasks:
            call_info = mocked_plugin_tasks[desc]
            if 'calls' in call_info:
                call_number = tasks_calls[desc]
                assert call_number <= len(call_info['calls']), "No info provide for the call {0} for task '{1}'"\
                    .format(call_number, desc)
                call_info = call_info['calls'][call_number - 1]
        # # Override timeout
        # if 'timeout' in attributes:
        #     attributes['timeout'] = 0
        _result = original_execute_plugin_for_item(args, attributes, desc, in_block, item, item_result_holder, name,
                                                   plugin, software_instance, _task_vars, index)
        if 'check_instance_vars' in call_info:
            for var, value in iteritems(call_info['check_instance_vars']):
                if var not in _task_vars.get('__instance__', {}):
                    assert "Missing expected var '{1}' for task '{0}'".format(desc, var)
                assert normalize(value) == normalize(_task_vars['__instance__'][var]), \
                    "Unexpected instance vars"
        return _result

    def mocked_execute_plugin_for_item_async(args, attributes, desc, in_block, item, item_result_holder,
                                             name, plugin, software_instance, timeout, index):
        call_info = {}
        if desc in mocked_plugin_tasks:
            call_info = mocked_plugin_tasks[desc]
            if 'calls' in call_info:
                call_number = tasks_calls[desc]
                assert call_number <= len(call_info['calls']), "No info provide for the call {0} for task '{1}'"\
                    .format(call_number, desc)
                call_info = call_info['calls'][call_number - 1]
        try:
            original_execute_plugin_for_item_async(args, attributes, desc, in_block, item, item_result_holder,
                                                   name, plugin, software_instance, timeout, index)
        except AssertionError:
            raise
        except Exception as e:
            if 'expected_exception' in call_info:
                expected_def = call_info['expected_exception']
                if 'type' in expected_def:
                    assert normalize(type(e).__name__) == normalize(expected_def['type']), \
                        "Exception expected for task '{0}' but different definition".format(desc)
                if 'message' in expected_def:
                    exp_msg = expected_def['message'].lower()
                    if exp_msg not in ('any', '*', '.*'):
                        assert exp_msg in str(e).lower(), \
                            "Exception expected for task '{0}' but different definition".format(desc)
            else:
                assert False, "Plugin for task '{0}' call '{2}' raised an unexpected exception: '{1}'"\
                    .format(desc, str(e), tasks_calls[desc])
            raise
        else:
            if 'expected_exception' in call_info:
                assert False, "Exception expected for task '{0}' call '{1}' but not raised"\
                    .format(desc, tasks_calls[desc])

    with patch.object(ActionModule, '_get_software_facts_plugin', new=mocked_get_software_facts_plugin):
        with patch.object(action_module, '_execute_plugin_for_item', new=mocked_execute_plugin_for_item):
            with patch.object(action_module, '_execute_plugin_for_item_async',
                              new=mocked_execute_plugin_for_item_async):
                result = action_module.process_software(task_vars=task_vars, **data)

    # Check expected plugins calls
    for task_name, task_info in iteritems(mocked_plugin_tasks):
        if 'calls' in task_info:
            assert 'number_of_calls' not in task_info or task_info['number_of_calls'] == len(task_info['calls']), \
                "'calls' length and 'number_of_calls' defined simultaneously with different values for task {0}" \
                .format(task_name)
            assert tasks_calls.get(task_name, 0) == len(task_info['calls']), \
                "Task '{0}' called {1} times and expected {2} times".format(
                    task_name, tasks_calls.get(task_name), len(task_info['calls']))
        if 'number_of_calls' in task_info:
            assert tasks_calls.get(task_name, 0) == task_info['number_of_calls'], \
                "Task '{0}' called {1} times and expected {2} times".format(
                    task_name, tasks_calls.get(task_name), task_info['number_of_calls'])

    if expected_tasks_calls is not None:
        # Remove 0 and any
        expected = {x: y for x, y in iteritems(expected_tasks_calls) if str(y).lower() not in ('0', 'any', '*', '.*')}
        actual = {x: y for x, y in iteritems(tasks_calls) if str(y).lower() not in ('0', 'any', '*', '.*')}
        if expected_tasks_calls_strict:
            assert normalize(actual) == normalize(expected), "Wrong call number in some task"
        else:
            non_existing = list(set(expected.keys()) - set(actual.keys()))
            assert not non_existing, "This expected_tasks_calls were not called: '{0}'".format(non_existing)
            assert normalize({x: y for x, y in iteritems(actual) if x in expected}) == normalize(expected), \
                "Wrong call number in some task"

    assert normalize(result) == normalize(expected_result)
