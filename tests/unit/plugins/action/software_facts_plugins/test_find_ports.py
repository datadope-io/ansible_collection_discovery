from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible.errors import AnsibleRuntimeError

from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.find_ports \
    import FindPorts as PluginToTest


def test_get_args_spec():
    assert PluginToTest.get_args_spec() == {
        'filter': {
            'type': 'dict',
            'required': False,
            'default': {}
        }
    }


@pytest.mark.parametrize(
    ('args', 'expected_result'),
    (
        (dict(filter={'foo': 'bar'}), True),
        (dict(), True),
        (dict(filter='fail'), False)
    )
)
def test_validate_args(action_module, args, expected_result):
    _action_module = action_module(ActionModule)
    plugin = PluginToTest(_action_module, {})

    if not expected_result:
        with pytest.raises(AnsibleRuntimeError) as exinfo:
            plugin.validate_args(args)
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'find_ports'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    args = {
        'filter': {
            'protocol': 'tcp'
        }
    }
    expected_result = [
        {
            "protocol": "tcp",
            "name": "service_1",
            "pid": 5410,
            "stime": "Tue Apr 26 15:54:44 2022",
            "address": "0.0.0.0",
            "port": 8080,
            "user": "root"
        },
        {
            "protocol": "tcp",
            "name": "service_2",
            "pid": 5410,
            "stime": "Tue Apr 26 15:54:44 2022",
            "address": "0.0.0.0",
            "port": 8080,
            "user": "root"
        }
    ]
    task_vars = {
        'tcp_listen': [
            {
                "protocol": "tcp",
                "name": "service_1",
                "pid": 5410,
                "stime": "Tue Apr 26 15:54:44 2022",
                "address": "0.0.0.0",
                "port": 8080,
                "user": "root"
            },
            {
                "protocol": "tcp",
                "name": "service_2",
                "pid": 5410,
                "stime": "Tue Apr 26 15:54:44 2022",
                "address": "0.0.0.0",
                "port": 8080,
                "user": "root"
            }
        ],
        'udp_listen': [
            {
                "protocol": "udp",
                "name": "service_3",
                "pid": 5410,
                "stime": "Tue Apr 26 15:54:44 2022",
                "address": "0.0.0.0",
                "port": 8080,
                "user": "root"
            }
        ]
    }

    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = PluginToTest(_action_module, task_vars)

    result = plugin.run(args, None, None)

    assert result == expected_result


def test_run_no_filter(action_module):
    args = {
        'filter': {}
    }
    expected_result = [
        {
            "protocol": "tcp",
            "name": "service_1",
            "pid": 5410,
            "stime": "Tue Apr 26 15:54:44 2022",
            "address": "0.0.0.0",
            "port": 8080,
            "user": "root"
        },
        {
            "protocol": "tcp",
            "name": "service_2",
            "pid": 5410,
            "stime": "Tue Apr 26 15:54:44 2022",
            "address": "0.0.0.0",
            "port": 8080,
            "user": "root"
        },
        {
            "protocol": "udp",
            "name": "service_3",
            "pid": 5410,
            "stime": "Tue Apr 26 15:54:44 2022",
            "address": "0.0.0.0",
            "port": 8080,
            "user": "root"
        }
    ]
    task_vars = {
        'tcp_listen': [
            {
                "protocol": "tcp",
                "name": "service_1",
                "pid": 5410,
                "stime": "Tue Apr 26 15:54:44 2022",
                "address": "0.0.0.0",
                "port": 8080,
                "user": "root"
            },
            {
                "protocol": "tcp",
                "name": "service_2",
                "pid": 5410,
                "stime": "Tue Apr 26 15:54:44 2022",
                "address": "0.0.0.0",
                "port": 8080,
                "user": "root"
            }
        ],
        'udp_listen': [
            {
                "protocol": "udp",
                "name": "service_3",
                "pid": 5410,
                "stime": "Tue Apr 26 15:54:44 2022",
                "address": "0.0.0.0",
                "port": 8080,
                "user": "root"
            }
        ]
    }

    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = PluginToTest(_action_module, task_vars)

    result = plugin.run(args, None, None)

    assert result == expected_result
