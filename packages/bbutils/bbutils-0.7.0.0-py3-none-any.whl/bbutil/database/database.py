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

import abc
from abc import ABCMeta
from dataclasses import dataclass, field
from typing import Optional, List

import bbutil

from bbutil.database.sqlite import SQLite
from bbutil.database.table import Table

__all__ = [
    "Database"
]


@dataclass
class Database(metaclass=ABCMeta):

    name: str = ""
    sqlite: Optional[SQLite] = None
    tables: List[Table] = field(default_factory=list)
    filename: str = ""

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def prepare(self, **kwargs) -> bool:
        pass

    @abc.abstractmethod
    def clear_data(self):
        pass

    def get_table(self, name: str) -> Optional[Table]:
        for _table in self.tables:
            if _table.name == name:
                return _table
        return None

    def clear(self):
        for _table in self.tables:
            _table.clear()

        self.clear_data()
        return

    def store(self) -> int:
        _count = 0
        for _table in self.tables:
            _count += _table.store()
        return _count

    def load(self) -> int:
        _count = 0
        for _table in self.tables:
            _count += _table.load()
        return _count

    def start(self) -> bool:
        self.init()

        if (self.name == "") or (self.filename == ""):
            bbutil.log.error("File- or database-name is missing!")
            return False

        self.sqlite = SQLite(name=self.name, filename=self.filename)

        self.sqlite.prepare()

        _check = self.prepare()
        if _check is False:
            bbutil.log.error("Preparation of tables has failed!")
            return False

        for _table in self.tables:
            _check = _table.init()
            if _check is False:
                return False
        return True
