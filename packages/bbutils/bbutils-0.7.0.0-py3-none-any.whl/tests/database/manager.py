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

import sqlite3
import os
import unittest
import unittest.mock as mock

from unittest.mock import Mock

from bbutil.database.sqlite.manager import Connection
from bbutil.utils import full_path

from tests.helper.sqlite import sqlite_operational_error, mock_operational_error

from tests.helper import set_log

__all__ = [
    "TestSQLiteManager"
]


class TestSQLiteManager(unittest.TestCase):
    """Testing class for locking module."""

    @staticmethod
    def _clean(filename: str, connection: sqlite3.Connection = None):
        if connection is not None:
            connection.close()

        if os.path.exists(filename) is True:
            os.remove(filename)
        return

    def setUp(self):
        set_log()
        return

    def test_setup_01(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        self.assertEqual(_connection.filename, _testfile)
        self.assertEqual(_connection.use_memory, False)
        self.assertIsNotNone(_connection._lock)
        return

    def test_setup_02(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(use_memory=True)

        self.assertEqual(_connection.filename, "")
        self.assertEqual(_connection.use_memory, True)
        self.assertIsNotNone(_connection._lock)
        return

    def test_abort_01(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()

        _connection.abort()
        self.assertIsNone(_connection._lock)

        _connection.setup(filename=_testfile, use_memory=False)

        _connection._lock.acquire()
        _connection.abort()
        return

    def test_reset_01(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        self.assertIsNotNone(_connection._lock)

        _check = _connection.connect()

        _con = _connection.connection

        self.assertIsNotNone(_connection.connection)

        _connection.reset()
        self.assertIsNone(_connection.connection)

        self._clean(_testfile, _con)
        return

    def test_connect_01(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        self.assertEqual(_connection.filename, _testfile)
        self.assertEqual(_connection.use_memory, False)
        self.assertIsNotNone(_connection._lock)

        _check = _connection.connect()
        c = _connection.cursor()
        self.assertTrue(_check)
        self.assertIsNotNone(_connection.connection)
        self.assertIsNotNone(c)

        _check = _connection.release()
        self.assertTrue(_check)
        return

    @mock.patch('sqlite3.connect', new=mock_operational_error)
    def test_connect_02(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        self.assertEqual(_connection.filename, _testfile)
        self.assertEqual(_connection.use_memory, False)
        self.assertIsNotNone(_connection._lock)

        _check = _connection.connect()
        c = _connection.cursor()
        self.assertFalse(_check)
        self.assertIsNone(_connection.connection)
        self.assertIsNone(c)

        _check = _connection.release()
        self.assertFalse(_check)
        return

    def test_connect_03(self):
        _connection = Connection()
        _connection.setup(use_memory=True)

        self.assertTrue(_connection.use_memory)
        self.assertIsNotNone(_connection._lock)

        _check = _connection.connect()
        c = _connection.cursor()
        self.assertTrue(_check)
        self.assertIsNotNone(_connection.connection)
        self.assertIsNotNone(c)

        _check = _connection.release()
        self.assertTrue(_check)
        return

    @mock.patch('sqlite3.connect', new=mock_operational_error)
    def test_connect_04(self):
        _connection = Connection()
        _connection.setup(use_memory=True)

        self.assertTrue(_connection.use_memory)
        self.assertIsNotNone(_connection._lock)

        _check = _connection.connect()
        c = _connection.cursor()
        self.assertFalse(_check)
        self.assertIsNone(_connection.connection)
        self.assertIsNone(c)

        _check = _connection.release()
        self.assertFalse(_check)
        return

    @mock.patch('sqlite3.connect', new=mock_operational_error)
    def test_connect_05(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        self.assertEqual(_connection.filename, _testfile)
        self.assertEqual(_connection.use_memory, False)
        self.assertIsNotNone(_connection._lock)

        _connection._connection = Mock()

        _check = _connection.connect()
        self.assertFalse(_check)
        return

    def test_release_01(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        _check = _connection.connect()
        self.assertTrue(_check)

        _check = _connection.release()
        self.assertTrue(_check)
        return

    def test_release_02(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        _check = _connection.release()
        self.assertFalse(_check)
        return

    def test_release_03(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection._connection = Mock()

        _check = _connection.release()
        self.assertFalse(_check)
        return

    def test_release_04(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        _connection._connection = Mock()
        _connection._connection.close = Mock(side_effect=sqlite_operational_error)

        _check = _connection.release()
        self.assertFalse(_check)
        return

    def test_commit_01(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        _check = _connection.connect()
        self.assertTrue(_check)

        _check = _connection.commit()
        self.assertTrue(_check)

        _check = _connection.release()
        self.assertTrue(_check)
        return

    def test_commit_02(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        _check = _connection.commit()
        self.assertFalse(_check)
        return

    def test_commit_03(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        _connection._connection = Mock()
        _connection._connection.commit = Mock(side_effect=sqlite_operational_error)

        _check = _connection.commit()
        self.assertFalse(_check)
        return
