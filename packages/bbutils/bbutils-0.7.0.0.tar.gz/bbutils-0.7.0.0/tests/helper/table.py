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

from bbutil.database import SQLite, Table, Types

__all__ = [
    "TestData",

    "get_table_01",
    "get_table_02",
    "get_table_03",
    "get_table_04"
]


def get_table_01(sqlite_object: SQLite) -> Table:
    _table = Table(name="tester01", sqlite=sqlite_object)
    _table.add_column(name="testid", data_type=Types.integer, unique=True, keyword=True)
    _table.add_column(name="use_test", data_type=Types.bool)
    _table.add_column(name="testname", data_type=Types.string)
    _table.add_column(name="path", data_type=Types.string)
    return _table


def get_table_02(sqlite_object: SQLite) -> Table:
    _table = Table(name="tester01", sqlite=sqlite_object)
    _table.add_column(name="testid", data_type=Types.integer, unique=True, keyword=True)
    _table.add_column(name="use_test", data_type=Types.bool)
    _table.add_column(name="testname", data_type=Types.string)
    _table.add_column(name="path", data_type=Types.string)
    _table.add_column(name="file", data_type=Types.string)
    return _table


def get_table_03(name: str, sqlite_object: SQLite) -> Table:
    _table = Table(name=name, sqlite=sqlite_object)
    _table.add_column(name="testid", data_type=Types.integer, primarykey=True)
    _table.add_column(name="use_test", data_type=Types.bool)
    _table.add_column(name="testname", data_type=Types.string)
    _table.add_column(name="path", data_type=Types.string)
    return _table


def get_table_04(sqlite_object: SQLite) -> Table:
    _table = Table(name="tester01", sqlite=sqlite_object)
    _table.add_column(name="testid", data_type=Types.integer, primarykey=True)
    _table.add_column(name="use_test", data_type=Types.bool)
    _table.add_column(name="category", data_type=Types.string, keyword=True)
    _table.add_column(name="testname", data_type=Types.string)
    _table.add_column(name="path", data_type=Types.string)
    return _table


class TestData(object):

    def __init__(self):
        self.testid: int = 0
        self.use_test: bool = False
        self.xcategory: str = ""
        self.testname: str = ""
        self.path: str = ""
        return
