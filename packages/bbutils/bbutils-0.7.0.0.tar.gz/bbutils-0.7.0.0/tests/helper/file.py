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

import os.path

__all__ = [
    "create_file"
]


def create_file(filename: str) -> bool:
    _path = os.path.dirname(filename)
    if os.path.exists(_path) is False:
        return False

    f = open(file=filename, mode="w")

    f.write("TEST!\n")

    f.close()
    return True
