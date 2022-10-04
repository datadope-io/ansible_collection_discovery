import json
import os

import pytest
import yaml

from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import MagicMock

from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionBase


@pytest.fixture(autouse=True)
def action_base_init_patch(monkeypatch):
    def _mocked_init(self, task=None, connection=None, play_context=None, loader=None, templar=None,
                     shared_loader_obj=None):
        self._task = task if task is not None else MagicMock()
        self._connection = connection if connection is not None else MagicMock()
        self._play_context = play_context if play_context is not None else MagicMock()
        self._loader = loader if loader is not None else MagicMock()
        self._templar = templar if templar is not None else MagicMock()
        self._shared_loader_obj = shared_loader_obj if shared_loader_obj is not None else MagicMock()
        return
    monkeypatch.setattr(ActionBase, "__init__", _mocked_init)


SUPPORTED_EXTENSIONS = ('.json', '.yaml', '.yml')

_no_default_marker = object()


def files_from_path(root_path, supported_extensions):
    """
    return: list of list of filenames. Each filename is a list
    """
    result = list()
    for root, dirs, files in os.walk(root_path):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for filename in files:
            _, extension = os.path.splitext(filename)
            if extension.lower() in supported_extensions:
                result.append([str(os.path.join(root, filename))])
    return result


def resources_files():
    return files_from_path(os.path.join(os.path.dirname(__file__), 'resources'), SUPPORTED_EXTENSIONS)


def pytest_configure():
    test_files = os.getenv('TEST_FILES', 'all')
    if test_files.lower() not in ('', 'all', '*', '.*'):
        filter_ = [x.strip() for x in test_files.split(',')]
        prefix = os.path.join(os.path.dirname(__file__), 'resources')
        files_to_include = []
        for f in filter_:
            files_to_include.append(f if f.startswith('/') else "{0}/{1}".format(prefix, f))
        pytest.file_list = [[f] for f in files_to_include]
    else:
        pytest.file_list = resources_files()


@pytest.fixture
def read_file():
    def _read_file(filepath, default=_no_default_marker):
        found = os.path.exists(filepath)
        if not found:
            _, ext = os.path.splitext(filepath)
            if not ext:
                found = False
                for ext in SUPPORTED_EXTENSIONS:
                    if os.path.exists(filepath + ext):
                        filepath = filepath + ext
                        found = True
                        break
        if not found:
            if default is _no_default_marker:
                raise FileNotFoundError(filepath)
            else:
                return default
        _, ext = os.path.splitext(filepath)
        with open(filepath, 'r') as f:
            if ext == '.json':
                return json.load(f)
            elif ext in ('.yaml', '.yml'):
                return yaml.load(f, yaml.SafeLoader)
            else:
                return f.read()

    return _read_file
