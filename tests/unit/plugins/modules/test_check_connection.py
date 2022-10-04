from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import socket

import ansible.module_utils.six.moves.urllib.error  # noqa
import pytest

import ansible_collections.datadope.discovery.plugins.modules.check_connection as module_to_test
from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import MagicMock, patch
from .conftest import AnsibleExitJson


def test_main(ansible_module_patch):
    ansible_args = {
        'address': '127.0.0.1',
        'port': 8080,
        'timeout': 1
    }
    ansible_module = ansible_module_patch(ansible_args=ansible_args.copy(),
                                          argument_spec=module_to_test.argument_spec,
                                          supports_check_mode=True)
    with pytest.raises(AnsibleExitJson) as result:
        with patch.object(module_to_test, 'setup_module_object', return_value=ansible_module) as mock_setup:
            with patch.object(module_to_test, 'validate_parameters', return_value=None) as mock_validate:
                with patch.object(module_to_test, 'check_port_open', return_value=True) as mock_check_port_open:
                    with patch.object(module_to_test, 'check_http_or_https', return_value='https') \
                            as mock_check_http_or_https:
                        module_to_test.main()
    mock_check_http_or_https.assert_called_once_with('127.0.0.1', 8080, 1)
    mock_check_port_open.assert_called_once_with('127.0.0.1', 8080, 1)
    mock_validate.assert_called_once_with(ansible_args)
    mock_setup.assert_called_once_with()
    assert result.value.args[0]['changed'] is False
    assert result.value.args[0]['available'] is True
    assert result.value.args[0]['identified_as'] == 'https'


def test_setup_module_object(module_args):
    ansible_args = {
        'address': '127.0.0.1',
        'port': 8080,
        'timeout': 1
    }
    module_args(ansible_args)
    module = module_to_test.setup_module_object()
    assert module.argument_spec == module_to_test.argument_spec
    assert module.supports_check_mode
    assert len(module.params) == 3


def test_validate_parameters(ansible_module_patch):
    ansible_args = {
        'address': '127.0.0.1',
        'port': 8080,
        'timeout': 1
    }
    ansible_module = ansible_module_patch(ansible_args=ansible_args.copy(),
                                          argument_spec=module_to_test.argument_spec,
                                          supports_check_mode=True)
    # TODO WHEN IMPLEMENTED
    # Fails if exception as function returns nothing
    assert module_to_test.validate_parameters(ansible_module.params) is None


def test_main_check_mode_true(ansible_module_patch):
    ansible_args = {
        'address': '127.0.0.1',
        'port': 8080,
        'timeout': 1
    }
    ansible_module = ansible_module_patch(ansible_args=ansible_args.copy(),
                                          argument_spec=module_to_test.argument_spec,
                                          supports_check_mode=True)
    with pytest.raises(AnsibleExitJson) as result:
        with patch.object(module_to_test, 'setup_module_object', return_value=ansible_module) as mock_setup:
            with patch.object(module_to_test, 'validate_parameters', return_value=None) as mock_validate:
                with patch.object(module_to_test, 'check_connection', return_value=(None, None)) \
                        as mock_check_connection:
                    module_to_test.main()
    mock_check_connection.assert_called_once_with(module=ansible_module)
    mock_validate.assert_called_once_with(ansible_args)
    mock_setup.assert_called_once_with()
    assert result.value.args[0]['changed'] is False
    assert result.value.args[0]['available'] is None
    assert result.value.args[0]['identified_as'] is None


def test_check_connection_check_mode_true():
    ansible_module_mock = MagicMock(spec=module_to_test.AnsibleModule)
    ansible_module_mock.check_mode = True
    assert module_to_test.check_connection(ansible_module_mock) == (None, None)


@patch('ansible.module_utils.six.moves.urllib.request.urlopen')
def test_check_http_or_https_endpoint_is_https(mocked_urlopen):
    assert module_to_test.check_http_or_https('127.0.0.1', 8080, 1) == 'https'
    mocked_urlopen.side_effect = ansible.module_utils.six.moves.urllib.error.HTTPError(None, None, None, None, None)
    assert module_to_test.check_http_or_https('127.0.0.1', 8080, 1) == 'https'


@patch('ansible.module_utils.six.moves.urllib.request.urlopen')
def test_check_http_or_https_endpoint_is_http(mocked_urlopen):
    mocked_urlopen.side_effect = [ansible.module_utils.six.moves.urllib.error.URLError(None),
                                  None]
    assert module_to_test.check_http_or_https('127.0.0.1', 8080, 1) == 'http'
    mocked_urlopen.side_effect = [ansible.module_utils.six.moves.urllib.error.URLError(None),
                                  ansible.module_utils.six.moves.urllib.error.HTTPError(None, None, None, None, None)]
    assert module_to_test.check_http_or_https('127.0.0.1', 8080, 1) == 'http'


@patch('ansible.module_utils.six.moves.urllib.request.urlopen')
def test_check_http_or_https_endpoint_is_none(mocked_urlopen):
    mocked_urlopen.side_effect = Exception('No endpoint')
    assert module_to_test.check_http_or_https('127.0.0.1', 8080, 1) is None
    mocked_urlopen.side_effect = [ansible.module_utils.six.moves.urllib.error.URLError(None),
                                  Exception('No endpoint')]
    assert module_to_test.check_http_or_https('127.0.0.1', 8080, 1) is None


@patch('socket.socket')
def test_check_port_open_open_port(mocked_socket):  # noqa
    assert module_to_test.check_port_open('127.0.0.1', 8080, 1) is True


@patch.object(socket.socket, 'connect')
def test_check_port_open_closed_port(socket_mock):
    socket_mock.side_effect = Exception('Connection error')
    assert module_to_test.check_port_open('127.0.0.1', 8080, 1) is False
