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

import os
import unittest
import unittest.mock as mock

from bbutil.database import Database

from tests.helper import set_log
from tests.helper.database import TestData

from tests.helper.sqlite import (mock_operational_error, sqlite_operational_error)

__all__ = [
    "TestDatabase"
]


class TestDatabase(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        return

    @staticmethod
    def _clean(database: Database):
        if database.sqlite is None:
            return

        _con = None

        if database.sqlite.manager is not None:
            _con = database.sqlite.manager.connection

        if _con is not None:
            _con.close()

        if os.path.exists(database.sqlite.filename) is True:
            os.remove(database.sqlite.filename)
        return

    def assertHasAttr(self, obj, intended_attr):
        _testBool = hasattr(obj, intended_attr)

        self.assertTrue(_testBool, msg=f'obj lacking an attribute. {obj=}, {intended_attr=}')
        return

    def test_start_01(self):
        _filename = "{0:s}/test.sqlite".format(os.getcwd())

        _database = TestData(filename=_filename)

        _check1 = _database.start()
        self.assertIsNotNone(_database.table01)
        self.assertIsNotNone(_database.table02)

        self._clean(_database)
        return

    def test_start_02(self):
        _database = TestData(filename="")

        _check1 = _database.start()
        self.assertFalse(_check1)

        self._clean(_database)
        return

    def test_start_03(self):
        _filename = "{0:s}/test.sqlite".format(os.getcwd())
        _database = TestData(filename=_filename, prepare_fail=True)

        _check1 = _database.start()

        self.assertFalse(_check1)
        self._clean(_database)
        return

    @mock.patch('sqlite3.connect', new=mock_operational_error)
    def test_start_04(self):
        _filename = "{0:s}/test.sqlite".format(os.getcwd())
        _database = TestData(filename=_filename)

        _check1 = _database.start()

        self.assertFalse(_check1)
        self._clean(_database)
        return

    def test_start_05(self):
        _filename = "{0:s}/testdata/database/test_database.sqlite".format(os.getcwd())
        _database = TestData(filename=_filename)

        _check1 = _database.start()
        self.assertIsNotNone(_database.table01)
        self.assertIsNotNone(_database.table02)
        return

    def test_get_table_01(self):
        _filename = "{0:s}/testdata/database/test_database.sqlite".format(os.getcwd())
        _database = TestData(filename=_filename)

        _check1 = _database.start()

        _table1 = _database.get_table("tester01")
        _table2 = _database.get_table("tester01XXXX")

        self.assertTrue(_check1)
        self.assertIsNotNone(_database.table01)
        self.assertIsNotNone(_database.table02)
        self.assertIsNotNone(_table1)
        self.assertIsNone(_table2)
        return

    def test_store_01(self):
        _filename = "{0:s}/test.sqlite".format(os.getcwd())

        if os.path.exists(_filename) is True:
            os.remove(_filename)

        _database = TestData(filename=_filename)

        _check1 = _database.start()
        self.assertIsNotNone(_database.table01)
        self.assertIsNotNone(_database.table02)

        _data = _database.table01.new_data()
        _data.use_test = False
        _data.testname = "01"
        _data.path = "//"

        _database.table01.add(_data)

        _data = _database.table02.new_data()
        _data.use_test = False
        _data.category = "01"
        _data.testname = "01"
        _data.path = "//"

        _database.table02.add(_data)

        _count3 = _database.store()

        _count1 = _database.table01.check()
        _count2 = _database.table02.check()

        self.assertTrue(_check1)
        self.assertEqual(_count1, 1)
        self.assertEqual(_count2, 1)
        self.assertEqual(_count3, 2)
        self._clean(_database)
        return

    def test_load_01(self):
        _filename = "{0:s}/testdata/database/test_database.sqlite".format(os.getcwd())
        _database = TestData(filename=_filename)

        _check1 = _database.start()
        self.assertIsNotNone(_database.table01)
        self.assertIsNotNone(_database.table02)

        _count = _database.load()

        self.assertTrue(_check1)
        self.assertEqual(_count, 2)
        self.assertEqual(_database.table01.data_count, 1)
        self.assertEqual(_database.table02.data_count, 1)
        return

    def test_clear_01(self):
        _filename = "{0:s}/testdata/database/test_database.sqlite".format(os.getcwd())
        _database = TestData(filename=_filename)

        _check1 = _database.start()
        self.assertIsNotNone(_database.table01)
        self.assertIsNotNone(_database.table02)

        _count = _database.load()

        self.assertTrue(_check1)
        self.assertEqual(_count, 2)
        self.assertEqual(_database.table01.data_count, 1)
        self.assertEqual(_database.table02.data_count, 1)

        _database.clear()
        self.assertEqual(_database.table01.data_count, 0)
        self.assertEqual(_database.table02.data_count, 0)
        return
