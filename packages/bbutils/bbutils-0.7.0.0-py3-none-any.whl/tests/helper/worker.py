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

from typing import List
from dataclasses import dataclass, field

import bbutil

from bbutil.worker import Worker

__all__ = [
    "CallManager",
    "Worker01",
    "Worker02"
]


@dataclass
class CallManager(object):

    start: int = 0
    stop: int = 0
    prepare: int = 0
    run: int = 0
    close: int = 0
    abort: int = 0

    def count(self, name: str):
        _value = getattr(self, name)
        _value += 1
        setattr(self, name, _value)
        return

    def setup(self, worker: Worker):
        worker.set_callback(start=lambda: self.count("start"))
        worker.set_callback(stop=lambda: self.count("stop"))
        worker.set_callback(prepare=lambda: self.count("prepare"))
        worker.set_callback(run=lambda: self.count("run"))
        worker.set_callback(close=lambda: self.count("close"))
        worker.set_callback(abort=lambda: self.count("abort"))
        return

    def info(self):
        bbutil.log.inform("start", "{0:d}".format(self.start))
        bbutil.log.inform("stop", "{0:d}".format(self.stop))
        bbutil.log.inform("prepare", "{0:d}".format(self.prepare))
        bbutil.log.inform("run", "{0:d}".format(self.run))
        bbutil.log.inform("close", "{0:d}".format(self.close))
        bbutil.log.inform("abort", "{0:d}".format(self.abort))
        return


@dataclass
class Worker01(Worker):

    exit_prepare: bool = True
    exit_run: bool = True
    exit_close: bool = True

    def init(self):
        self.set_id("Worker01")
        return

    def prepare(self) -> bool:
        return self.exit_prepare

    def run(self) -> bool:
        return self.exit_run

    def close(self) -> bool:
        return self.exit_close


@dataclass
class Worker02(Worker):

    max: int = 50000
    iterate_list: List[int] = field(default_factory=list)

    def init(self):
        self.set_id("Worker02")
        return

    def prepare(self) -> bool:
        _max = self.max
        _range = range(0, _max)
        _progress = bbutil.log.progress(_max)

        for n in _range:
            self.iterate_list.append(n)
            _progress.inc()

        bbutil.log.clear()
        return True

    def run(self) -> bool:
        _max = len(self.iterate_list)
        _progress = bbutil.log.progress(_max)

        n = 0
        for x in self.iterate_list:
            self.iterate_list[n] = x + 1
            _progress.inc()
            n += 1

        bbutil.log.clear()
        return True

    def close(self) -> bool:
        _max = len(self.iterate_list)
        _progress = bbutil.log.progress(_max)

        n = 0
        for x in self.iterate_list:
            self.iterate_list[n] = x - 1
            _progress.inc()
            n += 1

        bbutil.log.clear()
        return True
