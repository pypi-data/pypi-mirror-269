#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-04-24 18:34
# @Author  : Jack
# @File    : tools

"""
tools
"""

from os import environ
import socket


def hello():
    """
    初始化项目测试
    :return:
    """
    return "hello world!"


def get_env(key: str, default=None, value_type=None):
    """
        Returns the value from the key.
        check environment variables
    """
    value = default

    if key in environ:
        value = environ.get(key)

    if (value_type is None) or (default is None):
        return value

    if value_type == bool:
        return value == "True"

    return value_type(value)


def get_host_ip() -> str:
    """
        Returns the host ip.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('114.114.114.114', 80))
    return s.getsockname()[0]


def check_file_ext(filename: str, allowed_extensions=['png', 'jpg', 'jpeg']) -> bool:
    """
    检查文件扩展名是否符合要求
    :param filename:
    :param allowed_extensions:
    :return:
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
