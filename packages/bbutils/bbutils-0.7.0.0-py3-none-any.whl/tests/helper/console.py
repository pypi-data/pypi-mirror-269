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

import sys
import os

from dataclasses import dataclass

from bbutil.utils import full_path
from bbutil.logging import Logging
from bbutil.app import Console, Config

from testdata.app.config import AppConfig

__all__ = [
    "AppConsole"
]

_index = {
    0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    2: ["INFORM", "DEBUG1", "DEBUG2", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    3: ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]
}

if sys.platform == "win32":
    _filename1 = full_path("{0:s}/testdata/config01_win.json".format(os.getcwd()))
else:
    _filename1 = full_path("{0:s}/testdata/config01.json".format(os.getcwd()))


@dataclass
class AppConsole(Console):

    filename: str = ""
    return_start: bool = True
    return_stop: bool = True

    def create_logging(self) -> Logging:
        _log = Logging()
        _log.setup(app="Test", level=2, index=_index)

        console = _log.get_writer("console")
        _log.register(console)
        _log.open()
        return _log

    def create_config(self) -> Config:
        _work = "{0:s}/test".format(os.getcwd())
        if os.path.exists(_work) is False:
            os.mkdir(_work)

        _config = AppConfig(use_config=True, config_filename=self.filename)
        return _config

    def init(self):
        self.filename = _filename1
        return

    def start(self) -> bool:
        return self.return_start

    def stop(self) -> bool:
        return self.return_stop
