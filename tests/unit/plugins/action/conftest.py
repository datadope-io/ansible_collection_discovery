import pytest

from ansible.module_utils.six import iteritems
from ansible.template import Templar
from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import ANY, MagicMock, patch


@pytest.fixture
def action_module():
    def _action_module(class_, check_mode=False, task_vars=None):
        task_mock = MagicMock()
        task_mock.async_val = False
        play_context_mock = MagicMock()
        play_context_mock.check_mode = check_mode
        connection_mock = MagicMock()
        connection_mock._shell.tmpdir = None  # noqa
        loader_mock = MagicMock()
        shared_loader_obj_mock = MagicMock()
        if task_vars is None:
            templar_mock = MagicMock()
        else:
            templar_mock = Templar(loader_mock,
                                   shared_loader_obj=shared_loader_obj_mock,
                                   variables=task_vars)
        return class_(task_mock, connection_mock, play_context_mock, loader_mock, templar_mock, shared_loader_obj_mock)
    yield _action_module


@pytest.fixture(autouse=True)
def adjust_discovery_time():
    from ansible_collections.datadope.discovery.plugins.action.software_facts import GenericDetector

    class MyGenericDetector(GenericDetector):
        def __init__(self, software_config):
            super(MyGenericDetector, self).__init__(software_config)

        def get_software(self):
            sw_list = super(MyGenericDetector, self).get_software()
            for sw in sw_list:
                sw['discovery_time'] = ANY
            return sw_list

    patcher = patch('ansible_collections.datadope.discovery.plugins.action.software_facts.GenericDetector')

    def _create_detector(param):
        return MyGenericDetector(software_config=param)

    patched_class = patcher.start()
    patched_class.side_effect = _create_detector
    yield
    patcher.stop()


ANY_FLAGS = ('any', '*', '.*')


@pytest.fixture
def normalize():

    def _normalize(element, any_values=ANY_FLAGS):
        if isinstance(element, str):
            return ANY if element.lower() in any_values else element
        if isinstance(element, list):
            new_list = []
            for list_element in element:
                new_list.append(_normalize(list_element))
            return new_list
        if isinstance(element, dict):
            new_dict = {}
            for key, value in iteritems(element):
                new_dict[key] = _normalize(value)
            return new_dict
        return element

    yield _normalize
