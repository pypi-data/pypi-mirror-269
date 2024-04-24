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

import os
import sys
import unittest

import unittest.mock as mock

import bbutil
from bbutil.utils import full_path, openjson

from tests.helper import set_log, set_module
from tests.helper.config import (MockArgumentParser01, MockArgumentParser02, MockArgumentParser03,
                                 MockArgumentParser04, MockArgumentParser05, mock_open)

from testdata.app.config import AppConfig

__all__ = [
    "TestConfig"
]

oserror = OSError("Something strange did happen!")
mock_oserror = mock.Mock(side_effect=oserror)
mock_remove = mock.Mock()

if sys.platform == "win32":
    _ls = "dir.bat"
else:
    _ls = "/usr/bin/ls"


class TestConfig(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        set_module()
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser01)
    def test_init_01(self):
        self.assertIsNotNone(bbutil.module)

        _work = full_path("{0:s}/test".format(os.getcwd()))
        if os.path.exists(_work) is False:
            os.mkdir(_work)

        _config = AppConfig(use_parser=True)

        _check2 = _config.init()
        self.assertTrue(_check2)
        self.assertTrue(_config.valid)
        self.assertEqual(_config.verbose, 0)
        self.assertEqual(_config.bla, "/usr/local/bin/bla")
        self.assertEqual(_config.bleb, 10)
        self.assertEqual(_config.ls, _ls)
        self.assertEqual(_config.work, _work)
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser01)
    def test_init_02(self):
        self.assertIsNotNone(bbutil.module)

        _config = AppConfig(use_parser=False)

        _check2 = _config.init()
        self.assertTrue(_check2)
        self.assertTrue(_config.valid)
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser01)
    def test_init_03(self):
        bbutil.module = None

        # noinspection PyTypeChecker
        bbutil.set_module(None)
        self.assertIsNone(bbutil.module)

        _config = AppConfig(use_parser=True)

        _check2 = _config.init()
        self.assertFalse(_check2)
        self.assertFalse(_config.valid)
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser02)
    def test_init_04(self):
        self.assertIsNotNone(bbutil.module)

        _config = AppConfig(use_parser=True)

        _check2 = _config.init()
        self.assertFalse(_check2)
        self.assertFalse(_config.valid)
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser03)
    def test_init_05(self):
        self.assertIsNotNone(bbutil.module)

        _config = AppConfig(use_parser=True)

        _check2 = _config.init()
        self.assertFalse(_check2)
        self.assertFalse(_config.valid)
        return

    def test_init_06(self):
        self.assertIsNotNone(bbutil.module)

        _work = full_path("{0:s}/test".format(os.getcwd()))
        if os.path.exists(_work) is False:
            os.mkdir(_work)

        if sys.platform == "win32":
            _filename = full_path("{0:s}/testdata/config01_win.json".format(os.getcwd()))
        else:
            _filename = full_path("{0:s}/testdata/config01.json".format(os.getcwd()))

        _config = AppConfig(use_config=True, config_filename=_filename)

        _check2 = _config.init()
        self.assertTrue(_check2)
        self.assertTrue(_config.valid)
        self.assertEqual(_config.verbose, 0)
        self.assertEqual(_config.bla, "/usr/local/bin/bla")
        self.assertEqual(_config.bleb, 10)
        self.assertEqual(_config.ls, _ls)
        self.assertEqual(_config.work, _work)
        return

    def test_init_07(self):
        self.assertIsNotNone(bbutil.module)

        _config = AppConfig(use_config=True, config_filename="pufffy")

        _check2 = _config.init()
        self.assertFalse(_check2)
        self.assertFalse(_config.valid)
        return

    def test_init_08(self):
        self.assertIsNotNone(bbutil.module)

        if sys.platform == "win32":
            _filename = full_path("{0:s}/testdata/config02_win.json".format(os.getcwd()))
        else:
            _filename = full_path("{0:s}/testdata/config02.json".format(os.getcwd()))

        _config = AppConfig(use_config=True, config_filename=_filename)

        _check2 = _config.init()
        self.assertFalse(_check2)
        self.assertFalse(_config.valid)
        return

    def test_init_09(self):
        self.assertIsNotNone(bbutil.module)

        _filename = full_path("{0:s}/testdata/config03.json".format(os.getcwd()))
        _config = AppConfig(use_config=True, config_filename=_filename)

        _check2 = _config.init()
        self.assertFalse(_check2)
        self.assertFalse(_config.valid)
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser04)
    def test_init_10(self):
        self.assertIsNotNone(bbutil.module)

        _config = AppConfig(use_parser=True)

        _check2 = _config.init()
        self.assertFalse(_check2)
        self.assertFalse(_config.valid)
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser05)
    def test_init_11(self):
        self.assertIsNotNone(bbutil.module)

        _config = AppConfig(use_parser=True)

        _check2 = _config.init()
        self.assertFalse(_check2)
        self.assertFalse(_config.valid)
        return

    def test_init_12(self):
        self.assertIsNotNone(bbutil.module)

        if sys.platform == "win32":
            _filename = full_path("{0:s}/testdata/config04_win.json".format(os.getcwd()))
        else:
            _filename = full_path("{0:s}/testdata/config04.json".format(os.getcwd()))

        _config = AppConfig(use_config=True, config_filename=_filename)

        _check2 = _config.init()
        self.assertFalse(_check2)
        self.assertFalse(_config.valid)
        return

    def test_store_01(self):
        self.assertIsNotNone(bbutil.module)

        _work = full_path("{0:s}/test".format(os.getcwd()))
        if os.path.exists(_work) is False:
            os.mkdir(_work)

        if sys.platform == "win32":
            _filename1 = full_path("{0:s}/testdata/config01_win.json".format(os.getcwd()))
        else:
            _filename1 = full_path("{0:s}/testdata/config01.json".format(os.getcwd()))

        _filename2 = full_path("{0:s}/config01.json".format(os.getcwd()))

        _config = AppConfig(use_config=True, config_filename=_filename1)
        _check2 = _config.init()

        if os.path.exists(_filename2) is True:
            os.remove(_filename2)

        _config.config_filename = _filename2

        _check3 = _config.store()
        _check4 = os.path.exists(_filename2)

        _data = openjson(_filename2)
        if os.path.exists(_filename2) is True:
            os.remove(_filename2)

        self.assertTrue(_check2)
        self.assertTrue(_check3)
        self.assertTrue(_check4)
        self.assertTrue(_config.valid)

        self.assertEqual(_data["verbose"], 0)
        self.assertEqual(_data["bla"], "/usr/local/bin/bla")
        self.assertEqual(_data["bleb"], 10)
        self.assertEqual(_data["ls"], _ls)
        self.assertEqual(_data["work"], _work)
        return

    def test_store_02(self):
        self.assertIsNotNone(bbutil.module)

        _work = full_path("{0:s}/test".format(os.getcwd()))
        if os.path.exists(_work) is False:
            os.mkdir(_work)

        if sys.platform == "win32":
            _filename1 = full_path("{0:s}/testdata/config01_win.json".format(os.getcwd()))
        else:
            _filename1 = full_path("{0:s}/testdata/config01.json".format(os.getcwd()))

        _filename2 = full_path("{0:s}/config01.json".format(os.getcwd()))

        _config = AppConfig(use_config=True, config_filename=_filename1)
        _check2 = _config.init()

        if os.path.exists(_filename2) is True:
            os.remove(_filename2)

        _config.use_config = False

        _check3 = _config.store()
        _check4 = os.path.exists(_filename2)

        self.assertTrue(_check2)
        self.assertTrue(_check3)
        self.assertFalse(_check4)
        self.assertTrue(_config.valid)
        return

    def test_store_03(self):
        self.assertIsNotNone(bbutil.module)

        _work = full_path("{0:s}/test".format(os.getcwd()))
        if os.path.exists(_work) is False:
            os.mkdir(_work)

        if sys.platform == "win32":
            _filename1 = full_path("{0:s}/testdata/config01_win.json".format(os.getcwd()))
        else:
            _filename1 = full_path("{0:s}/testdata/config01.json".format(os.getcwd()))

        _filename2 = full_path("{0:s}/config01.json".format(os.getcwd()))

        _config = AppConfig(use_config=True, config_filename=_filename1)
        _check2 = _config.init()

        if os.path.exists(_filename2) is True:
            os.remove(_filename2)

        _config.config_filename = ""

        _check3 = _config.store()
        _check4 = os.path.exists(_filename2)

        self.assertTrue(_check2)
        self.assertFalse(_check3)
        self.assertFalse(_check4)
        self.assertFalse(_config.valid)
        return

    def test_store_04(self):
        self.assertIsNotNone(bbutil.module)

        _work = full_path("{0:s}/test".format(os.getcwd()))
        if os.path.exists(_work) is False:
            os.mkdir(_work)

        if sys.platform == "win32":
            _filename1 = full_path("{0:s}/testdata/config01_win.json".format(os.getcwd()))
        else:
            _filename1 = full_path("{0:s}/testdata/config01.json".format(os.getcwd()))

        _filename2 = full_path("{0:s}/config01.json".format(os.getcwd()))

        _config = AppConfig(use_config=True, config_filename=_filename1)
        _check2 = _config.init()

        if os.path.exists(_filename2) is True:
            os.remove(_filename2)

        _config.config_filename = _filename2

        with mock.patch('builtins.open', new=mock_open):
            _check3 = _config.store()

        _check4 = os.path.exists(_filename2)

        self.assertTrue(_check2)
        self.assertFalse(_check3)
        self.assertFalse(_check4)
        self.assertTrue(_config.valid)
        return
