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

from typing import List, Optional

from tkinter import Text
from tkinter.constants import END
from tkinter.ttk import Progressbar

from bbutil.logging.types import Writer, Message
from bbutil.utils import get_terminal_size

__all__ = [
    "TkWriter"
]

classname = "TkWriter"
_index = ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]

_schemes = {
    "NORMAL": "",
    "INFORM": "green",
    "DEBUG1": "cyan",
    "DEBUG2": "cyan",
    "DEBUG3": "cyan",
    "WARN": "magenta",
    "ERROR": "red",
    "EXCEPTION": "red",
    "TIMER": "yellow"
}


class TkWriter(Writer):

    def __init__(self):
        Writer.__init__(self, "TkLogger", _index)

        self.text_control: Optional[Text] = None
        self.progress_control: Optional[Progressbar] = None

        self.encoding: str = ""
        self.text_space: int = 15
        self.text_size: int = 11
        self.seperator: str = "|"
        self.length: int = 0
        self.error_index: List[str] = ["ERROR", "EXCEPTION"]

        size_x, size_y = get_terminal_size()

        self.line_width: int = size_x
        self.bar_len: int = 50
        self.active: bool = False
        return

    def setup(self, **kwargs):
        item = kwargs.get("text_space", None)
        if item is not None:
            self.text_space = item

        item = kwargs.get("seperator", None)
        if item is not None:
            self.seperator = item

        item = kwargs.get("error_index", None)
        if item is not None:
            self.error_index = item

        item = kwargs.get("bar_len", None)
        if item is not None:
            self.bar_len = item

        item = kwargs.get("text_size", None)
        if item is not None:
            self.text_size = item

        item = kwargs.get("text_control", None)
        if item is not None:
            self.text_control = item
            self._set_schemmes()

        item = kwargs.get("progress_control", None)
        if item is not None:
            self.progress_control = item
        return

    def _set_schemmes(self):
        for _key in _schemes:
            _value = _schemes[_key]
            if _value == "":
                self.text_control.tag_config(_key, font=("Monospace", self.text_size))
            else:
                self.text_control.tag_config(_key, font=("Monospace", self.text_size), foreground=_value)
        return

    def open(self) -> bool:
        if self.text_control is None:
            return False

        if self.progress_control is None:
            return False

        self.active = True
        return True

    def close(self) -> bool:  # pragma: no cover
        self.active = False
        return True

    def clear(self) -> bool:
        self.progress_control.configure(value=0)
        return True

    def _set_progress(self, item: Message):
        value = int(float(item.progress.counter * 100) / float(item.progress.limit))
        self.progress_control.configure(value=value)
        return

    def write(self, item: Message):
        if item.level == "PROGRESS":
            self._set_progress(item)
            return

        if self.active is False:
            return

        if item.tag == "":
            text = "{0:s}\n".format(item.content)
            self.text_control.insert(END, text, item.level)
            self.text_control.see(END)
        else:
            tag = item.tag.ljust(self.text_space)
            text = "{0:s} {1:s}\n".format(self.seperator, item.content)

            self.text_control.insert(END, tag, item.level)
            self.text_control.insert(END, text, "NORMAL")
            self.text_control.see(END)
        return
