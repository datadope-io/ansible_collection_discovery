from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes  # noqa

import pytest


@pytest.fixture
def module_args():
    """Fixture to manage arguments passing to module"""
    def _module_args(args):
        """Manages argument passing to module"""
        if '_ansible_remote_tmp' not in args:
            args['_ansible_remote_tmp'] = '/tmp'
        if '_ansible_keep_remote_files' not in args:
            args['_ansible_keep_remote_files'] = False

        args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
        basic._ANSIBLE_ARGS = to_bytes(args)
    yield _module_args


# FIXTURES TO MANAGE exit_json and fail_json

class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def fake_exit_json(*args, **kwargs):  # noqa
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fake_fail_json(*args, **kwargs):  # noqa
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


@pytest.fixture
def fail_json(monkeypatch):
    def _fail_json(ansible_module):
        monkeypatch.setattr(ansible_module, 'fail_json', fake_fail_json)
    yield _fail_json


@pytest.fixture
def exit_json(monkeypatch):
    def _exit_json(ansible_module):
        monkeypatch.setattr(ansible_module, 'exit_json', fake_exit_json)
    yield _exit_json


@pytest.fixture
def ansible_module_patch(exit_json, fail_json, module_args):
    """
    Return an AnsibleModule object to handle exit_json and fail_json and module input parameters.

    Using autouse=True this fixture is executed before every test.
    """
    def _ansible_module(ansible_args, *args, **kwargs):
        module_args(ansible_args)
        ansible_module = basic.AnsibleModule(*args, **kwargs)
        exit_json(ansible_module)
        fail_json(ansible_module)
        return ansible_module

    yield _ansible_module
