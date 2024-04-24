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

from typing import Optional
from unittest.mock import Mock

__all__ = [
    "CatchBacks",
    "MockPopen1",
    "MockPopen2",
    "MockPopen3"
]


class CatchBacks(object):

    def __init__(self):
        self.stdout = []
        self.stderr = []
        return

    def add_stdout(self, data):
        if data is None:
            return
        self.stdout.append(data)
        return

    def add_stderr(self, data):
        if data is None:
            return
        self.stderr.append(data)
        return


def get_stdout() -> list:

    _line1 = "TEST"

    _excec = UnicodeDecodeError('funnycodec', _line1.encode(), 1, 2, 'This is just a fake reason!')

    _line2 = Mock()
    _line2.decode = Mock(side_effect=_excec)

    _stdout = [
        _line1.encode(),
        _line2,
        None
    ]
    return _stdout


def get_stderr() -> list:
    _line1 = "ERROR!"

    _stderr = [
        _line1.encode(),
        None
    ]

    return _stderr


class MockPopen1(object):

    def __init__(self, commands, stdout, stderr, stdin=None):

        self.test_stdout = stdout
        self.test_stderr = stderr
        self.test_stdin = stdin
        self._poll = 0
        self.stdout = get_stdout()
        self.stderr = []
        self.returncode = 0
        return

    def poll(self) -> Optional[int]:
        if self._poll == 10:
            self._poll = 0
            return 1
        self._poll += 1
        return None


class MockPopen2(object):

    def __init__(self, commands, stdout, stderr, stdin=None):

        self.test_stdout = stdout
        self.test_stderr = stderr
        self.test_stdin = stdin
        self._poll = 0
        self.stdout = get_stdout()
        self.stderr = get_stderr()
        self.returncode = 1
        return

    def poll(self) -> Optional[int]:
        if self._poll == 10:
            self._poll = 0
            return 1
        self._poll += 1
        return None


class MockPopen3(object):

    def __init__(self, commands, stdout, stderr, stdin=None):

        self.test_stdout = stdout
        self.test_stderr = stderr
        self.test_stdin = stdin
        self._poll = 0
        self.stdout = get_stdout()
        self.stderr = []
        self.returncode = 1
        return

    def poll(self) -> Optional[int]:
        if self._poll == 10:
            self._poll = 0
            return 1
        self._poll += 1
        return None
