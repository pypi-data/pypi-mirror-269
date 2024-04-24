#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    Copyright (C) 2017, Kai Raphahn <kai.raphahn@laburec.de>
#

import sys

from unittest.mock import Mock

__all__ = [
    "MockArgumentParser01",
    "MockArgumentParser02",
    "MockArgumentParser03",
    "MockArgumentParser04",
    "MockArgumentParser05",
    "mock_open"
]

mock_open = Mock(side_effect=OSError("BUMM!"))

if sys.platform == "win32":
    _ls = "dir.bat"
else:
    _ls = "/usr/bin/ls"


class _Options01(object):

    def __init__(self):
        self.bla = "/usr/local/bin/bla"
        self.bleb = 10
        self.verbose = 0
        self.ls = _ls
        self.work = "test"
        return


class MockArgumentParser01(object):

    def __init__(self):
        self.add_argument = Mock()
        self.parse_args = Mock(return_value=_Options01())
        return


class _Options02(object):

    def __init__(self):
        self.bla = "/usr/local/bin/bla"
        self.bleb = 10
        self.ls = _ls
        self.work = "test"
        return


class MockArgumentParser02(object):

    def __init__(self):
        self.add_argument = Mock()
        self.parse_args = Mock(return_value=_Options02())
        return


class _Options03(object):

    def __init__(self):
        self.bla = "/usr/local/bin/bla"
        self.bleb = 10
        self.verbose = 0
        self.work = "test"
        return


class MockArgumentParser03(object):

    def __init__(self):
        self.add_argument = Mock()
        self.parse_args = Mock(return_value=_Options03())
        return


class _Options04(object):

    def __init__(self):
        self.bla = "/usr/local/bin/bla"
        self.bleb = 10
        self.verbose = 0
        self.ls = "/usr/toilet/ls"
        self.work = "test"
        return


class MockArgumentParser04(object):

    def __init__(self):
        self.add_argument = Mock()
        self.parse_args = Mock(return_value=_Options04())
        return


class _Options05(object):

    def __init__(self):
        self.bla = "/usr/local/bin/bla"
        self.bleb = 10
        self.verbose = 0
        self.ls = ""
        self.work = "test"
        return


class MockArgumentParser05(object):

    def __init__(self):
        self.add_argument = Mock()
        self.parse_args = Mock(return_value=_Options05())
        return
