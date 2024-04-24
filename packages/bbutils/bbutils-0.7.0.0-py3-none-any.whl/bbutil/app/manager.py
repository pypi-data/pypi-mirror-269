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

from bbutil.app.module import Module

__all__ = [
    "ModuleManager"
]


class ModuleManager(object):

    def __init__(self):
        self.modules: List[Module] = []
        self.commands: List[str] = []
        return

    def init(self, config: list) -> bool:

        for _config in config:
            _module = Module(**_config)

            self.commands.append(_module.command)
            self.modules.append(_module)
        return True

    def has_command(self, command: str) -> bool:
        if command in self.commands:
            return True
        return False

    def get_command(self, command_id: str) -> Optional[Module]:

        for _module in self.modules:
            if _module.command == command_id:
                return _module
        return None
