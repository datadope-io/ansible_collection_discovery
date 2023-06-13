from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import os

import pytest
from pytest_lazyfixture import lazy_fixture

from ansible_collections.community.internal_test_tools.tools.lib.yaml import load_yaml
from ansible_collections.datadope.discovery.plugins.action_utils.snmp_utils.utils import get_info_by_sysobject


@pytest.fixture
def sysobject_ids_file():
    return load_yaml(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "resources/sysobject_ids.yaml"
        ))


@pytest.fixture
def aruba_match_generic(sysobject_ids_file):
    params = {
        'sysobject_ids_file': sysobject_ids_file,
        'sysObjectId': "1.3.6.1.4.1.14823.1.1.32"
    }

    expected_result = {
        'template': 'generic_template',
        'brand': 'Aruba',
        'model': '7210 Controller',
        'snmp_type': 'NETWORKING'
    }

    return params, expected_result


@pytest.fixture
def aruba_not_brand_generic(sysobject_ids_file):
    params = {
        'sysobject_ids_file': sysobject_ids_file,
        'sysObjectId': "1.3.6.1.4.1.14823.1.1.33"
    }

    expected_result = {
        'template': 'generic_template',
        'brand': 'Aruba',
        'snmp_type': 'NETWORKING'
    }

    return params, expected_result


@pytest.fixture
def cisco_match_generic(sysobject_ids_file):
    params = {
        'sysobject_ids_file': sysobject_ids_file,
        'sysObjectId': "1.3.6.1.4.1.9.1.151"
    }

    expected_result = {
        'template': 'generic_template',
        'brand': 'Cisco',
        'model': 'Catalyst 116C',
        'snmp_type': 'NETWORKING'
    }

    return params, expected_result


@pytest.fixture
def cisco_match_testing(sysobject_ids_file):
    params = {
        'sysobject_ids_file': sysobject_ids_file,
        'sysObjectId': "1.3.6.1.4.1.9.1.150"
    }

    expected_result = {
        'template': 'testing_template',
        'brand': 'Cisco',
        'model': 'Catalyst 116T',
        'snmp_type': 'NETWORKING'
    }

    return params, expected_result


@pytest.fixture
def dell_not_type_generic(sysobject_ids_file):
    params = {
        'sysobject_ids_file': sysobject_ids_file,
        'sysObjectId': "1.3.6.1.4.1.674.10892.99"
    }

    expected_result = {
        'template': 'generic_template',
        'brand': 'Dell',
        'snmp_type': 'UNKNOWN'
    }

    return params, expected_result


@pytest.fixture
def dell_match_generic(sysobject_ids_file):
    params = {
        'sysobject_ids_file': sysobject_ids_file,
        'sysObjectId': "1.3.6.1.4.1.674.10892.5"
    }

    expected_result = {
        'template': 'generic_template',
        'brand': 'Dell',
        'model': 'PowerEdge',
        'snmp_type': 'NETWORKING'
    }

    return params, expected_result


@pytest.mark.parametrize(argnames=['params_and_expected_result'],
                         argvalues=[
                             (lazy_fixture('aruba_match_generic'),),
                             (lazy_fixture('aruba_not_brand_generic'),),
                             (lazy_fixture('cisco_match_generic'),),
                             (lazy_fixture('cisco_match_testing'),),
                             (lazy_fixture('dell_not_type_generic'),),
                             (lazy_fixture('dell_match_generic'),), ]
                         )
def test_sysobjectids(params_and_expected_result):
    params, expected_result = params_and_expected_result
    result = get_info_by_sysobject(
        sysobject_ids_file=params['sysobject_ids_file'],
        snmp_sysobjectid=params['sysObjectId']
    )

    assert result == expected_result
