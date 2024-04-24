#!/usr/bin/python3
# coding=utf-8

# Copyright (C) 2020, Siemens Healthcare Diagnostics Products GmbH
# Licensed under the Siemens Inner Source License 1.2, see LICENSE.md.

import abc
import os.path
import argparse

import json

from dataclasses import dataclass
from abc import ABCMeta
from typing import Optional

from bbutil.utils import check_object, check_dict, openjson

import bbutil

__all__ = [
    "Config"
]


@dataclass
class Config(metaclass=ABCMeta):

    _is_valid: bool = False

    config_filename: str = ""
    use_parser: bool = False
    use_config: bool = False
    parser: Optional[argparse.ArgumentParser] = None
    verbose: int = 0

    @property
    def valid(self) -> bool:
        return self._is_valid

    @staticmethod
    def check_path(input_path) -> bool:
        if input_path == "":
            bbutil.log.error("Invalid path!")
            return False

        if os.path.exists(input_path) is False:
            bbutil.log.error("Unable to find: {0:s}".format(input_path))
            return False
        return True

    def prepare_parser(self) -> bool:
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser()

        if bbutil.module is None:
            bbutil.log.error("Module manager is missing!")
            return False

        commands = []

        for _module in bbutil.module.modules:
            commands.append(_module.command)

        self.parser.add_argument("command", help="commands to run, use <command> -h for more help",
                                 choices=commands)

        self.parser.add_argument("-v", "--verbose", help="increase output verbosity", type=int,
                                 default=0, choices=[0, 1, 2])
        return True

    @abc.abstractmethod
    def setup_parser(self):
        pass

    @abc.abstractmethod
    def read_parser(self, options) -> bool:
        pass

    def _read_parser(self) -> bool:
        options = self.parser.parse_args()

        check = check_object(options, ["verbose"])
        if check is False:
            bbutil.log.error("Parser results are invalid!")
            return False

        self.verbose = options.verbose

        check = self.read_parser(options)
        if check is False:
            bbutil.log.error("Reading config from parser has failed!")
            return False
        return True

    def _init_parser(self) -> bool:
        if self.use_parser is False:
            return True

        check = self.prepare_parser()
        if check is False:
            return False

        self.setup_parser()

        check = self._read_parser()
        if check is False:
            return False

        return True

    @abc.abstractmethod
    def parse_config(self, config: dict) -> bool:
        pass

    def _load_config(self) -> bool:
        if self.use_config is False:
            return True

        if os.path.exists(self.config_filename) is False:
            bbutil.log.error("Config not found: {0:s}".format(self.config_filename))
            return False

        _config = openjson(self.config_filename)

        check = check_dict(_config, ["verbose"])
        if check is False:
            bbutil.log.error("Config is invalid!")
            return False

        check = self.parse_config(_config)
        if check is False:
            bbutil.log.error("Reading config from file has failed!")
            return False
        return True

    @abc.abstractmethod
    def create_config(self) -> dict:
        pass

    def store(self) -> bool:
        if self.use_config is False:
            return True

        if self.config_filename == "":
            self._is_valid = False
            bbutil.log.error("No filename for storing!")
            return False

        _config = self.create_config()
        _data = json.dumps(_config, indent=4)

        bbutil.log.inform("Config", "Store {0:s}".format(self.config_filename))

        try:
            f = open(file=self.config_filename, mode="w")
        except OSError as e:
            bbutil.log.exception(e)
            return False

        f.write(_data)
        f.close()
        return True

    @abc.abstractmethod
    def check_config(self) -> bool:
        pass

    def init(self) -> bool:
        if (self.use_config is False) and (self.use_parser is False):
            self._is_valid = True
            return True

        check = self._init_parser()
        if check is False:
            return False

        check = self._load_config()
        if check is False:
            return False

        check = self.check_config()
        if check is False:
            bbutil.log.error("Config check has failed!")
            return False

        self._is_valid = True
        return True
