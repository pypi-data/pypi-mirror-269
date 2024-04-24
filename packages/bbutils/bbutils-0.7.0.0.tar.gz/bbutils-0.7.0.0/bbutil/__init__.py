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

from typing import Optional
from bbutil.logging import Logging
from bbutil.app.config import Config
from bbutil.app.manager import ModuleManager

__all__ = [
    "app",
    "database",
    "lang",
    "logging",
    "worker",

    "data",
    "execute",
    "file",
    "setup",
    "utils",

    "log",
    "config",
    "module",

    "set_log",
    "set_config",
    "set_module"
]


#: package name
__name__ = "bbutils"

#: package author
__author__ = "Kai Raphahn"

#: email of package maintainer
__email__ = "kai.raphahn@laburec.de"

#: copyright year
__year__ = 2024

#: package copyright
__copyright__ = "Copyright (C) {0:d}, {1:s} <{2:s}>".format(__year__, __author__, __email__)

#: package description
__description__ = "Small collection of stuff for all my other python projects (including logging)."

#: package license
__license__ = "Apache License, Version 2.0"

#: package credits
__credits__ = [__author__]

#: version milestone
__milestone__ = 0

#: version major
__major__ = 7

#: version minor
__minor__ = 0

#: version patch
__patch__ = 0

#: package version
__version__ = "{0:d}.{1:d}.{2:d}.{3:d}".format(__milestone__, __major__, __minor__, __patch__)

#: package maintainer
__maintainer__ = __author__


log: Optional[Logging] = None
config: Optional[Config] = None
module: Optional[ModuleManager] = None


def set_log(item: Logging):
    global log
    log = item
    return


def set_config(item: Config):
    global config
    config = item
    return


def set_module(item: ModuleManager):
    global module
    module = item
    return
