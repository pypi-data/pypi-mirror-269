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
import threading
import time

from abc import ABCMeta
from dataclasses import dataclass
from typing import Optional

import bbutil
from bbutil.worker.callback import Callback

__all__ = [
    "Worker",

    "callback"
]


@dataclass
class Worker(metaclass=ABCMeta):

    abort: bool = False
    interval: float = 0.01

    _id: str = ""
    _callback: Optional[Callback] = None
    _error: bool = False
    _running: bool = True

    def __post_init__(self):
        self.init()
        return

    @property
    def id(self) -> str:
        return self._id

    @property
    def error(self) -> bool:
        return self._error

    def set_id(self, new_id: str):
        self._id = new_id
        return

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def prepare(self) -> bool:
        pass

    @abc.abstractmethod
    def run(self) -> bool:
        pass

    @abc.abstractmethod
    def close(self) -> bool:
        pass

    def set_callback(self, **kwargs):
        if self._callback is None:
            self._callback = Callback()

        self._callback.set_callback(**kwargs)
        return

    def _do_step(self, step: str, function, callback_func):
        if self.abort is True:
            self._running = False
            self.abort = False
            self._callback.do_abort()
            bbutil.log.warn(self._id, "Abort {0:s}".format(step))
            return

        callback_func()

        _check = function()
        if _check is False:
            self._error = True
            bbutil.log.error("{0:s}: {1:s} failed!".format(self.id, step))

        if self._error is True:
            self._running = False
        return

    def _execute(self):
        if self._callback is None:
            self._callback = Callback()

        self._running = True
        self._callback.do_start()

        bbutil.log.inform(self.id, "Execute")

        self._do_step("prepare", self.prepare, self._callback.do_prepare)
        if self._running is False:
            self._callback.do_stop()
            return

        self._do_step("run", self.run, self._callback.do_run)
        if self._running is False:
            self._callback.do_stop()
            return

        self._do_step("close", self.close, self._callback.do_close)
        if self._running is False:
            self._callback.do_stop()
            return

        self._callback.do_stop()
        self._running = False
        return

    def start(self):
        _t = threading.Thread(target=self._execute)
        _t.start()
        return

    @property
    def is_running(self):
        return self._running

    def wait(self):
        _run = True

        while _run is True:
            time.sleep(self.interval)

            if self._running is False:
                _run = False
        return

    def execute(self) -> bool:
        self._execute()

        if self._error is True:
            return False

        return True
