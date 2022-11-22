from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


import pytest
from pytest_lazyfixture import lazy_fixture

from ansible_collections.datadope.discovery.plugins.action_utils.snmp_utils.post_process import post_process


@pytest.fixture
def decode_hex():
    params = ["decode_hex", ["0", "testing", "0x74657374696e67"]]
    expected_result = ["0", "testing", "testing"]
    return params, expected_result


@pytest.fixture
def decode_mac():
    params = ["decode_mac", ["0", "0x001a1e0321e0", "00001a1e0321e0"]]
    expected_result = ["0", "001a1e0321e0", "00001a1e0321e0"]
    return params, expected_result


@pytest.fixture
def lookups_adminstatus():
    params = ["lookup_adminstatus", ["0", "1", "2", "3"]]
    expected_result = ["0", "up", "down", "testing"]
    return params, expected_result


@pytest.fixture
def lookup_operstatus():
    params = ["lookup_operstatus", ["0", "1", "2", "3", "4", "5", "6", "7"]]
    expected_result = ["0", "up", "down", "testing", "unknown",
                       "dormant", "notPresent", "lowerLayerDown"]
    return params, expected_result


@pytest.fixture
def unknown_method():
    params = ["unknown_method", ["0"]]
    expected_result = [None]
    return params, expected_result


@pytest.mark.parametrize(argnames=['params_and_expected_result'],
                         argvalues=[
                             (lazy_fixture('decode_hex'),),
                             (lazy_fixture('decode_mac'),),
                             (lazy_fixture('lookups_adminstatus'),),
                             (lazy_fixture('lookup_operstatus'),),
                             (lazy_fixture('unknown_method'),)]
                         )
def test_post_process(params_and_expected_result):
    params, expected_result = params_and_expected_result
    for i in range(len(params[1])):
        process_method = post_process(params[0])
        result = process_method(params[1][i]) if process_method else None
        assert result == expected_result[i]
