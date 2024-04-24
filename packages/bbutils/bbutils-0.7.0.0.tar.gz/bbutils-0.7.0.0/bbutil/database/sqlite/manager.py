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

from dataclasses import dataclass
from multiprocessing import Lock
from typing import Optional

import bbutil

__all__ = [
    "Connection"
]


@dataclass
class Connection(object):

    use_memory: bool = False
    filename: str = ""

    _lock: Optional[Lock] = None
    _connection: Optional[sqlite3.Connection] = None
    _cursor: Optional[sqlite3.Cursor] = None

    @property
    def connection(self) -> Optional[sqlite3.Connection]:
        return self._connection

    def cursor(self) -> Optional[sqlite3.Cursor]:
        if self._connection is not None:
            return self._connection.cursor()
        return None

    def setup(self, **kwargs):
        if self._lock is None:
            self._lock = Lock()

        _value = kwargs.get("use_memory", None)
        if _value is not None:
            self.use_memory = _value

        _value = kwargs.get("filename", None)
        if _value is not None:
            self.filename = _value
        return

    def _connect_memory(self) -> bool:
        try:
            self._connection = sqlite3.connect(':memory:',
                                               detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        except sqlite3.OperationalError as e:
            self._connection = None
            bbutil.log.error("Unable to create database in memory!")
            bbutil.log.exception(e)
            return False

        self.filename = "memory"
        return True

    def _connect_file(self) -> bool:
        try:
            self._connection = sqlite3.connect(self.filename,
                                               detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        except sqlite3.OperationalError as e:
            bbutil.log.error("Unable to create database: {0:s}".format(self.filename))
            bbutil.log.exception(e)
            return False

        bbutil.log.debug1("SQLite3", "Connect to {0:s}".format(self.filename))
        return True

    def connect(self) -> bool:
        self._lock.acquire()

        if self._connection is not None:
            bbutil.log.error("Connection is still active!")
            return False

        if self.use_memory is True:
            _check = self._connect_memory()
        else:
            _check = self._connect_file()

        if _check is False:
            self._lock.release()

        return _check

    def commit(self) -> bool:
        if self._connection is None:
            bbutil.log.error("No connection!")
            return False

        try:
            self._connection.commit()
        except sqlite3.OperationalError as e:
            bbutil.log.error("Unable to commit to database!")
            bbutil.log.exception(e)
            return False
        return True

    def abort(self):
        if self._lock is None:
            return
        self._lock.release()
        return

    def reset(self):
        self._lock = Lock()
        self._connection = None
        return

    def release(self) -> bool:
        if self._connection is None:
            bbutil.log.error("No connection!")
            return False

        if self._lock is None:
            bbutil.log.error("No valid lock!")
            return False

        try:
            self._connection.close()
        except sqlite3.OperationalError as e:
            bbutil.log.error("Unable to close connection!")
            bbutil.log.exception(e)
            return False

        self._connection = None

        if self.use_memory is False:
            bbutil.log.debug1("SQLite3", "Close {0:s}".format(self.filename))

        self._lock.release()
        return True
