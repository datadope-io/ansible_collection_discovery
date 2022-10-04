#
# This file is part of apacheconfig software.
#
# Copyright (c) 2018-2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/apacheconfig/LICENSE.rst
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ApacheConfigError(Exception):
    pass


class ConfigFileReadError(ApacheConfigError):
    pass
