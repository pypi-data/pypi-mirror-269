# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-app-ui
# FileName:     dir.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/24
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import os
import sys
import typing as t


def get_project_path():
    # 获取当前执行文件的绝对路径（兼容 Python 2 和 Python 3）
    exec_file_path = os.path.abspath(sys.argv[0])
    exec_file_path_slice = exec_file_path.split(os.path.sep)
    return os.path.sep.join(exec_file_path_slice[:-1])


def get_images_dir():
    return os.path.join(get_project_path(), "static", "images")


def is_exists(file_name: t.LiteralString | str | bytes) -> bool:
    if os.path.exists(file_name):
        return True
    else:
        return False


def is_file(file_path: str):
    if os.path.isfile(file_path):
        return True
    else:
        return False


def is_dir(file_path: str):
    if os.path.isdir(file_path):
        return True
    else:
        return False


def join_path(path_slice: list) -> t.LiteralString | str | bytes:
    return os.path.join(*path_slice)
