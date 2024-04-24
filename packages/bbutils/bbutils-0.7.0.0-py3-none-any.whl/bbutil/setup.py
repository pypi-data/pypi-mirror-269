#!/usr/bin/python3
# coding=utf-8

# Copyright (C) 2020, Siemens Healthcare Diagnostics Products GmbH
# Licensed under the Siemens Inner Source License 1.2, see LICENSE.md.

import os

from bbutil.utils import full_path, fix_sep


__all__ = [
    "find_data_files"
]


def _find_folders(path: str, folders: list, exlude_list: list):
    for root, dirs, files in os.walk(path, topdown=True):
        for name in sorted(dirs):

            _item = full_path("{0:s}/{1:s}".format(root, name))

            do_continue = False

            for _exclude in exlude_list:
                if _exclude in _item:
                    do_continue = True

            if do_continue is True:
                continue

            if "__pycache__" in _item:
                continue

            folders.append(_item)
    return


def _find_files(path: str, current_path: str, exlude_list: list) -> list:
    _files = []
    for _item in sorted(os.listdir(path)):

        _fullname = full_path("{0:s}/{1:s}".format(path, _item))
        _path = _fullname.replace(current_path, "")

        if "__pycache__" in _fullname:
            continue

        do_continue = False

        for _exclude in exlude_list:
            if _exclude in _item:
                do_continue = True

        if do_continue is True:
            continue

        if os.path.isdir(_fullname) is True:
            continue

        _path = fix_sep(_path)
        _files.append(_path)
    return _files


def find_data_files(folder: str, target: str, package_files: list, exlude_list: list):
    current_path = "{0:s}{1:s}".format(os.getcwd(), os.sep)
    target_folder = full_path("{0:s}/{1:s}".format(current_path, folder))

    _folders = [
        target_folder
    ]

    _find_folders(target_folder, _folders, exlude_list)

    for _item in _folders:
        _files = _find_files(_item, current_path, exlude_list)

        _target_folder = "{0:s}{1:s}".format(target_folder, os.sep)
        _name = _item.replace(_target_folder, "")

        if _name == target_folder:
            _name = target
        else:
            _name = "{0:s}/{1:s}".format(target, _name)
            _name = fix_sep(_name)

        _count = len(_files)
        if _count == 0:
            continue

        package_data = (_name, _files)
        package_files.append(package_data)
    return
