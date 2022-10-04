from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible.errors import AnsibleRuntimeError

from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionModule
from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.plugins.builtin.find_packages \
    import FindPackages as PluginToTest


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
        assert exinfo.value.message.startswith("Wrong parameters sent to software facts plugin 'find_packages'")
    else:
        plugin.validate_args(args)


def test_run(action_module):
    args = {
        'filter': {
            'name': 'package_2'
        }
    }
    expected_result = [
        {
            "name": "package_2",
            "source": "rpm",
            "epoch": None,
            "version": "352c64e5",
            "release": "52ae6884",
            "arch": None
        },
        {
            "name": "package_2",
            "source": "rpm",
            "epoch": None,
            "version": "f4a80eb5",
            "release": "53a7ff4b",
            "arch": None
        }
    ]
    task_vars = {
        'packages': {
            'package_1': [
                {
                    "name": "package_1",
                    "source": "rpm",
                    "epoch": None,
                    "version": "352c64e5",
                    "release": "52ae6884",
                    "arch": None
                }
            ],
            'package_2': [
                {
                    "name": "package_2",
                    "source": "rpm",
                    "epoch": None,
                    "version": "352c64e5",
                    "release": "52ae6884",
                    "arch": None
                },
                {
                    "name": "package_2",
                    "source": "rpm",
                    "epoch": None,
                    "version": "f4a80eb5",
                    "release": "53a7ff4b",
                    "arch": None
                }
            ],
            'package_3': [
                {
                    "name": "package_3",
                    "source": "rpm",
                    "epoch": None,
                    "version": "352c64e5",
                    "release": "52ae6884",
                    "arch": None
                }
            ]
        }
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
            "name": "package_1",
            "source": "rpm",
            "epoch": None,
            "version": "352c64e5",
            "release": "52ae6884",
            "arch": None
        },
        {
            "name": "package_2",
            "source": "rpm",
            "epoch": None,
            "version": "352c64e5",
            "release": "52ae6884",
            "arch": None
        },
        {
            "name": "package_2",
            "source": "rpm",
            "epoch": None,
            "version": "f4a80eb5",
            "release": "53a7ff4b",
            "arch": None
        },
        {
            "name": "package_3",
            "source": "rpm",
            "epoch": None,
            "version": "352c64e5",
            "release": "52ae6884",
            "arch": None
        }
    ]
    task_vars = {
        'packages': {
            'package_1': [
                {
                    "name": "package_1",
                    "source": "rpm",
                    "epoch": None,
                    "version": "352c64e5",
                    "release": "52ae6884",
                    "arch": None
                }
            ],
            'package_2': [
                {
                    "name": "package_2",
                    "source": "rpm",
                    "epoch": None,
                    "version": "352c64e5",
                    "release": "52ae6884",
                    "arch": None
                },
                {
                    "name": "package_2",
                    "source": "rpm",
                    "epoch": None,
                    "version": "f4a80eb5",
                    "release": "53a7ff4b",
                    "arch": None
                }
            ],
            'package_3': [
                {
                    "name": "package_3",
                    "source": "rpm",
                    "epoch": None,
                    "version": "352c64e5",
                    "release": "52ae6884",
                    "arch": None
                }
            ]
        }
    }

    _action_module = action_module(ActionModule)
    _action_module._templar.template = lambda x: x
    plugin = PluginToTest(_action_module, task_vars)

    result = plugin.run(args, None, None)

    assert result == expected_result
