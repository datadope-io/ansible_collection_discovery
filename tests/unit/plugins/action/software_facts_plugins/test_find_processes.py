from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible.errors import AnsibleRuntimeError

from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.find_processes \
    import FindProcesses as PluginToTest


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
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'find_processes'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    args = {
        'filter': {
            'pid': '1071'
        }
    }
    expected_result = [
        {
            "cmdline": "/usr/sbin/sshd -D",
            "cwd": "/usr/sbin/",
            "pid": "1071",
            "ppid": "1",
            "user": "root"
        }
    ]
    task_vars = {
        "processes": [
            {
                "cmdline": "/usr/lib/systemd/systemd --switched-root --system --deserialize 21",
                "pid": "1",
                "ppid": "0",
                "user": "root",
                "cwd": "/usr/lib/systemd/"
            },
            {
                "cmdline": "/usr/sbin/sshd -D",
                "pid": "1071",
                "ppid": "1",
                "user": "root",
                "cwd": "/usr/sbin/"
            },
            {
                "cmdline": "/usr/sbin/crond -n",
                "pid": "1073",
                "ppid": "1",
                "user": "root",
                "cwd": "/usr/sbin/"
            },
            {
                "cmdline": "/sbin/agetty --keep-baud 115200,38400,9600 ttyS0 vt220",
                "pid": "1074",
                "ppid": "1",
                "user": "root",
                "cwd": "/sbin/"
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
            "cmdline": "/usr/lib/systemd/systemd --switched-root --system --deserialize 21",
            "pid": "1",
            "ppid": "0",
            "user": "root",
            "cwd": "/usr/lib/systemd/"
        },
        {
            "cmdline": "/usr/sbin/sshd -D",
            "pid": "1071",
            "ppid": "1",
            "user": "root",
            "cwd": "/usr/sbin/"
        },
        {
            "cmdline": "/usr/sbin/crond -n",
            "pid": "1073",
            "ppid": "1",
            "user": "root",
            "cwd": "/usr/sbin/"
        },
        {
            "cmdline": "/sbin/agetty --keep-baud 115200,38400,9600 ttyS0 vt220",
            "pid": "1074",
            "ppid": "1",
            "user": "root",
            "cwd": "/sbin/"
        }
    ]
    task_vars = {
        "processes": [
            {
                "cmdline": "/usr/lib/systemd/systemd --switched-root --system --deserialize 21",
                "cwd": "/usr/lib/systemd/",
                "pid": "1",
                "ppid": "0",
                "user": "root"
            },
            {
                "cmdline": "/usr/sbin/sshd -D",
                "cwd": "/usr/sbin/",
                "pid": "1071",
                "ppid": "1",
                "user": "root"
            },
            {
                "cmdline": "/usr/sbin/crond -n",
                "cwd": "/usr/sbin/",
                "pid": "1073",
                "ppid": "1",
                "user": "root"
            },
            {
                "cmdline": "/sbin/agetty --keep-baud 115200,38400,9600 ttyS0 vt220",
                "cwd": "/sbin/",
                "pid": "1074",
                "ppid": "1",
                "user": "root"
            }
        ]
    }

    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = PluginToTest(_action_module, task_vars)

    result = plugin.run(args, None, None)

    assert result == expected_result
