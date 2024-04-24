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

__all__ = [
    "testdata1",
    "testdata2"
]


testdata1 = [
    (
       "data",
       [
          "testdata/testos1.py",
          "testdata/testos2.py",
          "testdata/testos3.py"
       ]
    ),
    (
       "data/database",
       [
           "testdata/database/test_add_columns.sqlite",
           "testdata/database/test_bulk.sqlite",
           "testdata/database/test_check_table.sqlite",
           "testdata/database/test_database.sqlite",
           "testdata/database/test_select.sqlite",
           "testdata/database/test_update.sqlite"
       ]
    ),
    (
       "data/testlang",
       [
          "testdata/testlang/__init__.py"
       ]
    ),
    (
       "data/testlang/test1",
       [
          "testdata/testlang/test1/__init__.py",
          "testdata/testlang/test1/tester.py"
       ]
    ),
    (
       "data/testlang/test2",
       [
          "testdata/testlang/test2/__init__.py"
       ]
    )
]

testdata2 = [
    (
        'data/database',
        [
            "testdata/database/test_add_columns.sqlite",
            "testdata/database/test_bulk.sqlite",
            "testdata/database/test_check_table.sqlite",
            "testdata/database/test_database.sqlite",
            "testdata/database/test_select.sqlite",
            "testdata/database/test_update.sqlite"
        ]
    )
]
