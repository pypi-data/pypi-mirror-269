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
from unittest import mock as mock

from bbutil.database import SQLite, Types, Table, Data

__all__ = [
    "sqlite_unknown_error",
    "sqlite_operational_error",
    "sqlite_integrity_error",
    "mock_operational_error",

    "get_sqlite_operational_error",
    "get_sqlite_integrity_error",
    "get_sqlite_return_false",

    "get_table_01",
    "get_data_01",
    "get_data_02",
    "get_data_03",
    "get_data_04",
    "get_data_05",
    "get_data_06",
    "get_data_07",
    "get_data_08"
]

sqlite_unknown_error = Exception("Something strange did happen!")
sqlite_operational_error = sqlite3.OperationalError('This did go boing!!')
sqlite_integrity_error = sqlite3.IntegrityError('These values did go boing!!')
mock_operational_error = mock.Mock(side_effect=sqlite_operational_error)


def get_sqlite_operational_error():
    _cursor = mock.Mock(name="SQLite3.cursor")
    _cursor.execute = mock.Mock(side_effect=sqlite_operational_error)

    _connection = mock.Mock(name="SQLite3.connect")
    _connection.cursor = mock.Mock(return_value=_cursor)

    _sqlite = mock.Mock(name="SQLite3", return_value=_connection)
    return _sqlite


def get_sqlite_integrity_error():
    _cursor = mock.Mock(name="SQLite3.cursor")
    _cursor.execute = mock.Mock(side_effect=sqlite_integrity_error)

    _connection = mock.Mock(name="SQLite3.connect")
    _connection.cursor = mock.Mock(return_value=_cursor)

    _sqlite = mock.Mock(name="SQLite3", return_value=_connection)
    return _sqlite


def get_sqlite_return_false():
    _sqlite = mock.Mock(name="close", return_value=False)
    return _sqlite


def get_table_01(sqlite_object: SQLite) -> Table:
    _table = Table(name="tester01", sqlite=sqlite_object)
    _table.add_column(name="testid", data_type=Types.integer, unique=True)
    _table.add_column(name="use_test", data_type=Types.bool)
    _table.add_column(name="testname", data_type=Types.string)
    _table.add_column(name="path", data_type=Types.string)
    return _table


def get_data_01() -> Data:
    _names = [
        "testid",
        "use_test",
        "testname",
        "path"
    ]

    _values = [
        1,
        True,
        "Test01",
        "testers/"
    ]

    _data = Data(_names, _values)
    return _data


def get_data_02() -> Data:
    _names = [
        "testidx",
        "use_test",
        "testname",
        "path"
    ]

    _values = [
        1,
        True,
        "Test01",
        "testers/"
    ]

    _data = Data(_names, _values)
    return _data


def get_data_03() -> Data:
    _names = [
        "testid",
        "use_test",
        "testname",
        "path"
    ]

    _values = [
        15235670141346654134,
        True,
        "Test01",
        "testers/"
    ]

    _data = Data(_names, _values)
    return _data


def get_data_04() -> Data:
    _names = [
        "testid",
        "use_test",
        "testname",
        "path"
    ]

    _values = [
        1,
        True,
        "Test01",
        [
            "List1",
            "List2"
        ]
    ]

    _data = Data(_names, _values)
    return _data


def get_data_05() -> list:
    _names = [
        "testid",
        "use_test",
        "testname",
        "path"
    ]

    _values = [
        [1, True, "Test01", "testers/"],
        [2, True, "Test02", "testers/"],
        [3, True, "Test03", "testers/"],
        [4, False, "Test04", "testXXs/"],
        [5, True, "Test05", "testXXs/"],
        [6, True, "Test06", "testXXs/"]
    ]

    _datas = []

    for _value in _values:
        _data = Data(_names, _value)
        _datas.append(_data)
    return _datas


def get_data_06() -> list:
    _names = [
        "testid",
        "use_test",
        "testname",
        "path"
    ]

    _values = [
        [1, True, "Test01", "testers/"],
        [2, True, "Test02", "testers/"],
        [3, True, "Test03", "testers/"],
        [4, False, "Test04"],
        [5, True, "Test05", "testXXs/"],
        [6, True, "Test06", "testXXs/"]
    ]

    _datas = []

    for _value in _values:
        _data = Data(_names, _value)
        _datas.append(_data)
    return _datas


def get_data_07() -> Data:
    _names = [
        "testid",
        "use_test",
        "testname",
        "path"
    ]

    _values = [4, True, "Test04", "testXXs/"]

    _data = Data(_names, _values)
    return _data


def get_data_08() -> Data:
    _names = [
        "testid",
        "use_test",
        "testname",
        "path"
    ]

    _values = [4, True, "Test04", 15235670141346654134]

    _data = Data(_names, _values)
    return _data
