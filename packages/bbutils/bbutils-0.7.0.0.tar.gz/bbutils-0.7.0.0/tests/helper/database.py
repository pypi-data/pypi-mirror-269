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

from dataclasses import dataclass
from typing import Optional

from unittest.mock import Mock

from bbutil.database import Types, Table, Database

__all__ = [
    "TestData",
    "TestData2"
]


@dataclass
class TestData(Database):

    table01: Optional[Table] = None
    table02: Optional[Table] = None
    prepare_fail: bool = False
    mock_connection: Optional[Mock] = None

    def init(self):
        self.name = "Testos"
        return

    def prepare(self, **kwargs) -> bool:
        if self.prepare_fail is True:
            return False

        if self.mock_connection is not None:
            self.sqlite.connection = self.mock_connection

        _table = Table(name="tester01", sqlite=self.sqlite)
        _table.add_column(name="testid", data_type=Types.integer, primarykey=True)
        _table.add_column(name="use_test", data_type=Types.bool)
        _table.add_column(name="testname", data_type=Types.string)
        _table.add_column(name="path", data_type=Types.string)
        self.tables.append(_table)
        self.table01 = _table

        _table = Table(name="tester02", sqlite=self.sqlite)
        _table.add_column(name="testid", data_type=Types.integer, primarykey=True)
        _table.add_column(name="use_test", data_type=Types.bool)
        _table.add_column(name="category", data_type=Types.string, keyword=True)
        _table.add_column(name="testname", data_type=Types.string)
        _table.add_column(name="path", data_type=Types.string)
        self.tables.append(_table)
        self.table02 = _table
        return True

    def clear_data(self):
        return


@dataclass
class TestData2(Database):

    table01: Optional[Table] = None
    table02: Optional[Table] = None
    prepare_fail: bool = False
    mock_connection: Optional[Mock] = None

    def init(self):
        self.name = "Testos"
        return

    def prepare(self, **kwargs) -> bool:
        if self.prepare_fail is True:
            return False

        if self.mock_connection is not None:
            self.sqlite.connection = self.mock_connection

        _table = Table(name="tester01", sqlite=self.sqlite, version=1)
        _table.add_column(name="testid", data_type=Types.integer, primarykey=True)
        _table.add_column(name="use_test", data_type=Types.bool)
        _table.add_column(name="testname", data_type=Types.string)
        _table.add_column(name="path", data_type=Types.string)
        self.tables.append(_table)
        self.table01 = _table

        _table = Table(name="tester02", sqlite=self.sqlite)
        _table.add_column(name="testid", data_type=Types.integer, primarykey=True)
        _table.add_column(name="use_test", data_type=Types.bool)
        _table.add_column(name="category", data_type=Types.string, keyword=True)
        _table.add_column(name="testname", data_type=Types.string)
        _table.add_column(name="path", data_type=Types.string)
        self.tables.append(_table)
        self.table02 = _table
        return True

    def clear_data(self):
        return
