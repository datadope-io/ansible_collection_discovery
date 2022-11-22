# Copyright: (c) 2022, DataDope (@datadope-io)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


import binascii

from ansible.module_utils._text import to_text


def _decode_hex(hex_string):
    if len(hex_string) < 3:
        return hex_string
    if hex_string[:2] == "0x":
        return to_text(binascii.unhexlify(hex_string[2:]))
    return hex_string


def _decode_mac(hex_string):
    if len(hex_string) != 14:
        return hex_string
    if hex_string[:2] == "0x":
        return hex_string[2:]
    return hex_string


def _lookup_adminstatus(adminstatus):
    adminstatus_options = {
        '1': 'up',
        '2': 'down',
        '3': 'testing'
    }
    if adminstatus in adminstatus_options:
        return adminstatus_options[adminstatus]
    return adminstatus


def _lookup_operstatus(operstatus):
    operstatus_options = {
        '1': 'up',
        '2': 'down',
        '3': 'testing',
        '4': 'unknown',
        '5': 'dormant',
        '6': 'notPresent',
        '7': 'lowerLayerDown'
    }
    if operstatus in operstatus_options:
        return operstatus_options[operstatus]
    return operstatus


def post_process(method):
    if method == 'decode_hex':
        return _decode_hex
    elif method == 'decode_mac':
        return _decode_mac
    elif method == 'lookup_adminstatus':
        return _lookup_adminstatus
    elif method == 'lookup_operstatus':
        return _lookup_operstatus
    else:
        return None
