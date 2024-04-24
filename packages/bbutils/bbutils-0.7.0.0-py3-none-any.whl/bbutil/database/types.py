#!/usr/bin/python3
# coding=utf-8
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
from enum import Enum
from typing import Any

__all__ = [
    "select_interval",

    "DataType",
    "Types",
    "Data",
    "Column"
]


def select_interval(count) -> int:
    _interval = 1

    if count > 1000:
        _interval = 10

    if count > 10000:
        _interval = 100

    if count > 100000:
        _interval = 1000
    return _interval


@dataclass
class DataType(object):

    type: str = ""
    value: Any = None


class Types(Enum):

    none = DataType(type="NULL", value=None)
    json = DataType(type="JSON", value={})
    bool = DataType(type="BOOLEAN", value=False)
    datetime = DataType(type="timestamp", value=None)
    integer = DataType(type="INTEGER", value=0)
    biginteger = DataType(type="BIGINT", value=0)
    float = DataType(type="REAL", value=0.0)
    string = DataType(type="TEXT", value="")
    bytes = DataType(type="BLOB", value=b"")
    list = DataType(type="BLOB", value=b"")


class Data(object):

    def __init__(self, keys: list, values: list):
        for (key, value) in zip(keys, values):
            self.__dict__[key] = value
        return


@dataclass
class Column(object):

    name: str = ""
    primarykey: bool = False
    unique: bool = False
    type: Types = Types.none

    @property
    def create(self) -> str:
        _datatype: DataType = self.type.value

        if self.primarykey is True:
            _ret = '"{0:s}" INTEGER PRIMARY KEY AUTOINCREMENT'.format(self.name)
            return _ret

        _ret = '"{0:s}" {1:s}'.format(self.name, _datatype.type)
        return _ret
