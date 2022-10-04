import json
import os

import pytest

from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import MagicMock

from ansible_collections.datadope.discovery.plugins.action.software_facts import ActionBase


@pytest.fixture(autouse=True)
def action_base_init_patch(monkeypatch):
    def _mocked_init(*args, **kwargs):  # noqa
        self = args[0]
        self._task = args[1] if len(args) > 1 and args[1] is not None else MagicMock()
        self._connection = args[2] if len(args) > 2 and args[2] is not None else MagicMock()
        self._play_context = args[3] if len(args) > 3 and args[3] is not None else MagicMock()
        self._loader = args[4] if len(args) > 4 and args[4] is not None else MagicMock()
        self._templar = args[5] if len(args) > 5 and args[5] is not None else MagicMock()
        self._shared_loader_obj = args[6] if len(args) > 6 and args[6] is not None else MagicMock()
    monkeypatch.setattr(ActionBase, "__init__", _mocked_init)


@pytest.fixture
def read_json_file():
    test_dir = os.path.dirname(os.path.abspath(__file__))

    def _read_json_file(filename):
        if not os.path.isabs(filename):
            filename = os.path.join(test_dir, filename)
        with open(filename, "r") as f:
            return json.load(f)

    yield _read_json_file
