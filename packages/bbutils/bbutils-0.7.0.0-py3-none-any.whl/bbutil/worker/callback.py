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

__all__ = [
    "Callback"
]


class Callback(object):

    def __init__(self):
        self.start = None
        self.stop = None
        self.prepare = None
        self.run = None
        self.close = None
        self.abort = None
        return

    def set_callback(self, **kwargs):
        _value = kwargs.get("start", None)
        if _value is not None:
            self.start = _value

        _value = kwargs.get("stop", None)
        if _value is not None:
            self.stop = _value

        _value = kwargs.get("prepare", None)
        if _value is not None:
            self.prepare = _value

        _value = kwargs.get("run", None)
        if _value is not None:
            self.run = _value

        _value = kwargs.get("close", None)
        if _value is not None:
            self.close = _value

        _value = kwargs.get("abort", None)
        if _value is not None:
            self.abort = _value
        return

    def do_start(self):
        if self.start is None:
            return
        self.start()
        return

    def do_stop(self):
        if self.stop is None:
            return
        self.stop()
        return

    def do_prepare(self):
        if self.prepare is None:
            return
        self.prepare()
        return

    def do_run(self):
        if self.run is None:
            return
        self.run()
        return

    def do_close(self):
        if self.close is None:
            return
        self.close()
        return

    def do_abort(self):
        if self.abort is None:
            return
        self.abort()
        return
