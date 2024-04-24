#!/usr/bin/python3
# coding=utf-8

# Copyright (C) 2020, Siemens Healthcare Diagnostics Products GmbH
# Licensed under the Siemens Inner Source License 1.2, see LICENSE.md.

import abc
import os.path

from dataclasses import dataclass
from abc import ABCMeta

from bbutil.utils import full_path

import bbutil

__all__ = [
    "File",
    "Folder",
    "Base"
]


@dataclass
class Base(metaclass=ABCMeta):

    path: str = ""
    basename: str = ""

    @property
    def exists(self) -> bool:
        _check = os.path.exists(self.fullpath)
        return _check

    @property
    def fullpath(self) -> str:
        _filename = full_path("{0:s}/{1:s}".format(self.path, self.basename))
        return _filename

    @property
    def valid(self) -> bool:
        if self.path == "":
            return False

        if self.basename == "":
            return False
        return True

    @abc.abstractmethod
    def init(self) -> bool:
        pass

    def clear(self):
        self.basename = ""
        self.path = ""

        self.clear_object()
        return

    @property
    def check(self) -> bool:
        if self.valid is False:
            bbutil.log.error("Given filename is not valid!")
            return False

        if self.exists is False:
            bbutil.log.error("Given filename does not exists!")
            return False
        return True

    def open(self, filename: str) -> bool:
        self.basename = os.path.basename(filename)
        self.path = os.path.dirname(filename)

        if self.check is False:
            return False

        _check = self.open_file()
        return _check

    @abc.abstractmethod
    def clear_object(self):
        pass

    @abc.abstractmethod
    def open_file(self) -> bool:
        pass

    @abc.abstractmethod
    def create(self) -> bool:
        pass

    def _remove_file(self) -> bool:
        try:
            os.remove(self.fullpath)
        except OSError as e:
            bbutil.log.exception(e)
            return False

        if self.exists is True:
            bbutil.log.error("Unable to remove file!")
            return False

        return True

    def _remove_folder(self) -> bool:
        try:
            os.rmdir(self.fullpath)
        except OSError as e:
            bbutil.log.exception(e)
            return False

        if self.exists is True:
            bbutil.log.error("Unable to remove file!")
            return False

        return True

    def remove(self) -> bool:
        if self.valid is False:
            return True

        if self.exists is False:
            return True

        if os.path.isdir(self.fullpath) is True:
            _check = self._remove_folder()
        else:
            _check = self._remove_file()

        return _check


class File(Base):

    def init(self) -> bool:
        return True

    def clear_object(self):
        return

    def open_file(self) -> bool:
        return True

    def create(self) -> bool:
        return True


class Folder(Base):

    def init(self) -> bool:
        return True

    def clear_object(self):
        return

    def open_file(self) -> bool:
        return True

    def create(self) -> bool:
        if self.exists is False:
            try:
                os.mkdir(self.fullpath)
            except OSError as e:
                bbutil.log.exception(e)
                return False

        if self.exists is False:
            bbutil.log.error("Unable to create: {0:s}".format(self.fullpath))
            return False
        return True
