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

from shutil import copyfile

import bbutil
from bbutil.logging import Logging
from bbutil.app.manager import ModuleManager
from bbutil.database import SQLite
from bbutil.utils import full_path

__all__ = [
    "config",
    "console",
    "database",
    "execute",
    "file",
    "module",
    "setup",
    "sqlite",
    "table",
    "worker",

    "get_sqlite",
    "copy_sqlite",
    "set_log",
    "set_module",
    "reset_module"
]

_index = {
    0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    2: ["INFORM", "DEBUG1", "DEBUG2", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    3: ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]
}


def get_sqlite(filename: str, path: str = os.getcwd(), clean: bool = False) -> SQLite:
    _testfile = full_path("{0:s}/{1:s}".format(path, filename))
    _name = "Test"

    if (os.path.exists(_testfile) is True) and (clean is True):
        os.remove(_testfile)

    _sqlite = SQLite(filename=_testfile, name="Test")
    return _sqlite


def copy_sqlite(filename: str, path: str = os.getcwd(), clean: bool = False) -> SQLite:
    _sourcefile = full_path("{0:s}/{1:s}".format(path, filename))
    _name = "Test"
    _testfile = "{0:s}/{1:s}".format(os.getcwd(), filename)

    if os.path.exists(_testfile):
        os.remove(_testfile)

    copyfile(_sourcefile, _testfile)

    _sqlite = SQLite(filename=_testfile, name="Test")
    return _sqlite


def set_log():
    if bbutil.log is not None:
        return

    _log = Logging()
    _log.setup(app="Test", level=2, index=_index)

    console = _log.get_writer("console")
    _log.register(console)
    _log.open()

    bbutil.set_log(_log)
    return


_config_modules = [
    {
        "name": "testone",
        "command": "test01",
        "desc": "the first test",
        "workers": [
            {
                "path": "testdata.app.commands.prepact",
                "classname": "Worker01"
            },
            {
                "path": "testdata.app.commands.runact",
                "classname": "Worker02"
            }
        ]
    },
    {
        "name": "testtwo",
        "command": "test02",
        "desc": "the second test",
        "workers": [
            {
                "path": "testdata.app.commands.prepact",
                "classname": "Worker01"
            }
        ]
    },
    {
        "name": "testthree",
        "command": "test03",
        "desc": "the third test",
        "workers": [
            {
                "path": "testdata.app.commands.prepact2",
                "classname": "Worker03"
            }
        ]
    }
]


def set_module():
    if bbutil.module is not None:
        return

    _module = ModuleManager()
    _check = _module.init(_config_modules)

    if _check is False:
        return

    bbutil.set_module(_module)
    return


def reset_module():
    if bbutil.module is None:
        return

    bbutil.set_module(None)
    return
