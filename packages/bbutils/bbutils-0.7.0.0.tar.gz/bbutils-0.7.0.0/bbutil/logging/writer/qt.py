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

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QTextCursor
from PySide6.QtWidgets import QTextEdit, QProgressBar

from bbutil.logging.types import Writer, Message
from bbutil.utils import get_terminal_size

__all__ = [
    "QtWriter"
]

classname = "QtWriter"
_index = ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]

_schemes = {
    "NORMAL": QColor(Qt.black),
    "INFORM": QColor(Qt.darkGreen),
    "DEBUG1": QColor(Qt.cyan),
    "DEBUG2": QColor(Qt.cyan),
    "DEBUG3": QColor(Qt.cyan),
    "WARN": QColor(Qt.magenta),
    "ERROR": QColor(Qt.red),
    "EXCEPTION": QColor(Qt.red),
    "TIMER": QColor(Qt.yellow)
}


class QtWriter(Writer):

    def __init__(self):
        Writer.__init__(self, "TkLogger", _index)

        self.text_control: Optional[QTextEdit] = None
        self.progress_control: Optional[QProgressBar] = None

        self.progress_reset: bool = False
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

        self._prepared: bool = False
        self._buffer: List[Message] = []
        return

    @property
    def _is_ready(self) -> bool:
        if (self.text_control is None) or (self.progress_control is None):
            return False
        return True

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
            self._set_text()

        item = kwargs.get("progress_control", None)
        if item is not None:
            self.progress_control = item
        return

    def _set_text(self):
        if self.text_control is None:
            return

        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        font.setPointSize(self.text_size)

        self.text_control.setFont(font)
        return

    def open(self) -> bool:
        self._init_progress()
        self.active = True
        return True

    def close(self) -> bool:  # pragma: no cover
        self.active = False
        return True

    def clear(self) -> bool:
        self.progress_control.setValue(0)
        self.progress_control.reset()
        self.progress_reset = True
        return True

    def _init_progress(self):
        if self.progress_control is None:
            return
        self.progress_control.setMinimum(0)
        self.progress_control.setMaximum(100)
        self.progress_reset = False
        return

    def _set_progress(self, item: Message):
        if self.progress_reset is True:
            self._init_progress()
        value = int(float(item.progress.counter * 100) / float(item.progress.limit))
        self.progress_control.setValue(value)
        return

    def _write(self, item: Message):
        if item.level == "":
            item.level = "NORMAL"

        _color = _schemes[item.level]

        if item.tag == "":
            text = "{0:s}\n".format(item.content)

            self.text_control.setTextColor(_color)
            self.text_control.insertPlainText(text)
            self.text_control.setTextColor(QColor(Qt.black))
        else:
            tag = item.tag.ljust(self.text_space)
            text = "{0:s} {1:s}\n".format(self.seperator, item.content)

            self.text_control.setTextColor(_color)
            self.text_control.insertPlainText(tag)

            self.text_control.setTextColor(QColor(Qt.black))
            self.text_control.insertPlainText(text)

        self.text_control.moveCursor(QTextCursor.End)
        return

    def write(self, item: Message):
        if item.level == "PROGRESS":
            self._set_progress(item)
            return

        if self.active is False:
            return

        if self._is_ready is False:
            self._buffer.append(item)
            return

        for _item in self._buffer:
            self._write(_item)

        self._buffer.clear()

        self._write(item)
        return
