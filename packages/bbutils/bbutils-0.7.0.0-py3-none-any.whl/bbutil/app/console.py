#!/usr/bin/python3
# coding=utf-8

# Copyright (C) 2020, Siemens Healthcare Diagnostics Products GmbH
# Licensed under the Siemens Inner Source License 1.2, see LICENSE.md.

import abc
import sys

from dataclasses import dataclass, field
from typing import Optional, List
from abc import ABCMeta

import bbutil

from bbutil.logging import Logging
from bbutil.app.manager import ModuleManager
from bbutil.app.config import Config
from bbutil.app.module import Module

__all__ = [
    "Console"
]


@dataclass
class Console(metaclass=ABCMeta):

    command_id: str = ""
    module: Optional[Module] = None
    module_config: List[dict] = field(default_factory=list)

    def __post_init__(self):
        self.init()
        return

    def _set_command(self) -> bool:
        if bbutil.config is None:
            bbutil.log.error("Config is missing!")
            return False

        if self.command_id == "":
            command_names = sys.argv[1:]

            for _command in command_names:
                check = bbutil.module.has_command(_command)
                if check is False:
                    continue

                self.command_id = _command
                break

        if self.command_id == "":
            bbutil.config.prepare_parser()
            bbutil.config.parser.print_help()
            return False

        self.module = bbutil.module.get_command(self.command_id)
        bbutil.log.debug1("Console", self.command_id)
        return True

    @abc.abstractmethod
    def create_logging(self) -> Logging:
        pass

    @abc.abstractmethod
    def create_config(self) -> Config:
        pass

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def start(self) -> bool:
        pass

    @abc.abstractmethod
    def stop(self) -> bool:
        pass

    def _setup_module(self) -> bool:
        if len(self.module_config) == 0:
            bbutil.log.error("No modules!")
            return False

        _modules = ModuleManager()

        _modules.init(self.module_config)

        bbutil.set_module(_modules)
        return True

    def _setup_config(self) -> bool:
        _config = self.create_config()

        check = _config.init()
        if check is False:
            return False

        bbutil.set_config(_config)
        return True

    def setup(self) -> bool:
        _log = self.create_logging()
        bbutil.set_log(_log)

        _version = sys.version.replace('\n', '- ')
        bbutil.log.debug1("Python", _version)

        _check = self._setup_module()
        if _check is False:
            return False

        _check = self._setup_config()
        if _check is False:
            return False

        bbutil.log.setup(level=bbutil.config.verbose)
        return True

    def execute(self) -> int:
        check = self._set_command()
        if check is False:
            return -1

        bbutil.log.inform("App", "Start {0:s}".format(self.command_id))

        check = self.start()
        if check is False:
            return 1

        check = self.module.load()
        if check is False:
            return 2

        for _worker in self.module.workers:
            check = _worker.execute()
            if check is True:
                continue

            return 3

        check = self.stop()
        if check is False:
            return 4

        bbutil.log.close()
        return 0
