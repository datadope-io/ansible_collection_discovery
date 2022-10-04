from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import base64
import pytest

from ansible.errors import AnsibleRuntimeError
from ansible.module_utils.common.text.converters import to_bytes
from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import patch
from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.read_remote_file \
    import ReadRemoteFile


def test_get_args_spec():
    assert ReadRemoteFile.get_args_spec() == {
        'file_path': {
            'type': 'str',
            'required': True
        },
        'parser': {
            'required': False,
            'type': 'str'
        },
        'parser_params': {
            'required': False,
            'type': 'dict'
        },
        'in_docker': {
            'default': True,
            'required': False,
            'type': 'bool'
        },
        'delegate_reading': {
            'default': False,
            'required': False,
            'type': 'bool'
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        (dict(file_path='test'), True),
        (dict(file_path='1.0.0', other='other'), False),
        (dict(other='test'), False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = ReadRemoteFile(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'read_remote_file'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    file_contents = 'The file contents'

    args = {
        'file_path': 'the_path',
        'parser': None,
        'parser_params': None,
        'in_docker': True,
        'delegate_reading': False
    }
    sw_instance = {}

    _action_module = action_module(ActionModule)
    task_vars = {}
    plugin = ReadRemoteFile(_action_module, task_vars)

    with patch.object(plugin, '_execute_module') as mock_execute_module:
        mock_execute_module.return_value = {
            'content': base64.b64encode(to_bytes(file_contents)),
            'encoding': 'base64',
            'failed': False
        }
        result = plugin.run(args, None, sw_instance)

    mock_execute_module.assert_called_once_with(module_name='ansible.legacy.slurp',
                                                module_args={'src': args['file_path']},
                                                task_vars=task_vars)
    assert result == dict(content=file_contents, failed=False)


def test_run_non_existing(action_module):
    args = {
        'file_path': 'the_path',
        'parser': None,
        'parser_params': None,
        'in_docker': True,
        'delegate_reading': False
    }
    sw_instance = {}

    _action_module = action_module(ActionModule)
    plugin = ReadRemoteFile(_action_module, {})

    with patch.object(plugin, '_execute_module') as mock_execute_module:
        mock_execute_module.return_value = {
            'failed': True,
            'msg': 'File not found'
        }
        result = plugin.run(args, None, sw_instance)

    mock_execute_module.assert_called_once_with(module_name='ansible.legacy.slurp',
                                                module_args={'src': args['file_path']},
                                                task_vars={})
    assert result == dict(failed=True, msg="the remote file 'the_path' does not exist, not transferring")


def test_run_parse_key_value(action_module):
    file_contents = """data_directory = '/var/lib/pgsql/10/data'
hba_file = '/etc/postgresql/10/data/pg_hba.conf'
ident_file = '/etc/postgresql/10/data/pg_ident.conf'
external_pid_file = '/var/run/postgresql/10-data.pid'
listen_addresses = '0.0.0.0'
port = 5432
max_connections = 150
superuser_reserved_connections = 3
unix_socket_directories = '/var/run/postgresql,/tmp'
unix_socket_group = ''
unix_socket_permissions = 0777
bonjour = off
bonjour_name = ''
authentication_timeout = 60s
    """
    expected_result = dict(
        data_directory='/var/lib/pgsql/10/data',
        hba_file='/etc/postgresql/10/data/pg_hba.conf',
        ident_file='/etc/postgresql/10/data/pg_ident.conf',
        external_pid_file='/var/run/postgresql/10-data.pid',
        listen_addresses='0.0.0.0',
        port='5432',
        max_connections='150',
        superuser_reserved_connections='3',
        unix_socket_directories='/var/run/postgresql,/tmp',
        unix_socket_group='',
        unix_socket_permissions='0777',
        bonjour='off',
        bonjour_name='',
        authentication_timeout='60s',
    )
    args = {
        'file_path': 'the_path',
        'parser': 'key_value',
        'parser_params': {
            'delimiters': ['#', ' ']
        },
        'in_docker': True,
        'delegate_reading': False
    }

    sw_instance = {}
    task_vars = {}
    _action_module = action_module(ActionModule)
    plugin = ReadRemoteFile(_action_module, task_vars)

    with patch.object(plugin, '_execute_module') as mock_execute_module:
        mock_execute_module.return_value = {
            'content': base64.b64encode(to_bytes(file_contents)),
            'encoding': 'base64',
            'failed': False
        }
        result = plugin.run(args, None, sw_instance)

    mock_execute_module.assert_called_once_with(module_name='ansible.legacy.slurp',
                                                module_args={'src': args['file_path']},
                                                task_vars=task_vars)

    assert result == dict(parsed=expected_result, content=file_contents, failed=False)


def test_run_parse_non_existing(action_module):
    args = {
        'file_path': 'the_path',
        'parser': 'non_existing',
        'parser_params': None,
        'in_docker': True,
        'delegate_reading': False
    }
    sw_instance = {}

    _action_module = action_module(ActionModule)
    plugin = ReadRemoteFile(_action_module, {})

    with pytest.raises(AnsibleRuntimeError) as exinfo:
        plugin.run(args, None, sw_instance)

    assert exinfo.value.message == "Software Facts parser 'non_existing' not found"


def test_run_parse_error_verbosity_less_three(action_module):
    file_contents = "The file contents"
    invocations_display = dict(init=0, verbose=0, v=0, verbosity=0)

    class _MockedDisplay:  # noqa
        def __init__(self):
            invocations_display['init'] += 1
            self._verbosity = 1

        def verbose(self, *args, **kwargs):  # noqa
            invocations_display['verbose'] += 1

        def v(self, *args, **kwargs):  # noqa
            invocations_display['v'] += 1

        @property
        def verbosity(self):
            invocations_display['verbosity'] += 1
            return self._verbosity

    args = {
        'file_path': 'the_path',
        'parser': 'json',
        'parser_params': None,
        'in_docker': True,
        'delegate_reading': False
    }
    sw_instance = {}

    task_vars = {}
    _action_module = action_module(ActionModule)
    plugin = ReadRemoteFile(_action_module, task_vars)

    with patch.object(plugin, '_execute_module') as mock_execute_module:
        mock_execute_module.return_value = {
            'content': base64.b64encode(to_bytes(file_contents)),
            'encoding': 'base64',
            'failed': False
        }
        with patch('ansible_collections.datadope.discovery.plugins.action_utils'
                   '.software_facts.plugins.builtin.read_remote_file.display', new=_MockedDisplay()):
            result = plugin.run(args, None, sw_instance)

    mock_execute_module.assert_called_once_with(module_name='ansible.legacy.slurp',
                                                module_args={'src': args['file_path']},
                                                task_vars=task_vars)

    assert invocations_display['init'] == 1
    assert invocations_display['verbosity'] == 1
    assert invocations_display['v'] == 1
    assert invocations_display['verbose'] == 0
    assert result.get('failed') is True


def test_run_parse_error_verbosity_three(action_module):
    file_contents = "The file contents"
    invocations_display = dict(init=0, verbose=0, v=0, verbosity=0)

    class _MockedDisplay:  # noqa
        def __init__(self):
            invocations_display['init'] += 1
            self._verbosity = 3

        def verbose(self, *args, **kwargs):  # noqa
            invocations_display['verbose'] += 1

        def v(self, *args, **kwargs):  # noqa
            invocations_display['v'] += 1

        @property
        def verbosity(self):
            invocations_display['verbosity'] += 1
            return self._verbosity

    args = {
        'file_path': 'the_path',
        'parser': 'json',
        'parser_params': None,
        'in_docker': True,
        'delegate_reading': False
    }
    sw_instance = {}

    task_vars = {}
    _action_module = action_module(ActionModule)
    plugin = ReadRemoteFile(_action_module, task_vars)

    with patch.object(plugin, '_execute_module') as mock_execute_module:
        mock_execute_module.return_value = {
            'content': base64.b64encode(to_bytes(file_contents)),
            'encoding': 'base64',
            'failed': False
        }
        with patch('ansible_collections.datadope.discovery.plugins.action_utils'
                   '.software_facts.plugins.builtin.read_remote_file.display', new=_MockedDisplay()):
            result = plugin.run(args, None, sw_instance)

    mock_execute_module.assert_called_once_with(module_name='ansible.legacy.slurp',
                                                module_args={'src': args['file_path']},
                                                task_vars=task_vars)

    assert invocations_display['init'] == 1
    assert invocations_display['verbosity'] == 1
    assert invocations_display['v'] == 0
    assert invocations_display['verbose'] == 1
    assert result.get('failed') is True
