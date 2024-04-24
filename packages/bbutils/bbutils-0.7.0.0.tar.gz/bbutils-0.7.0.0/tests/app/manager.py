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

import unittest

import unittest.mock as mock

from bbutil.app.manager import ModuleManager

from tests.helper import set_log, reset_module
from tests.helper.module import config_modules


__all__ = [
    "TestManager"
]

oserror = OSError("Something strange did happen!")
mock_oserror = mock.Mock(side_effect=oserror)
mock_remove = mock.Mock()


class TestManager(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        reset_module()
        return

    def test_init_01(self):
        _module = ModuleManager()
        _check1 = _module.init(config_modules)

        _command1 = _module.get_command("test01")
        _command2 = _module.get_command("test01xx")
        _check2 = _module.has_command("test01")
        _check3 = _module.has_command("test01xx")

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertFalse(_check3)
        self.assertIsNotNone(_command1)
        self.assertIsNone(_command2)
        self.assertEqual(len(_module.commands), 3)
        self.assertEqual(len(_module.modules), 3)
        return
