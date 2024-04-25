#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-04-25 13:39
# @Author  : Jack
# @File    : PyString

"""
PyString
"""
import random
import string


def get_random_id(length: int = 10) -> str:
    """
    生成指定长度的随机字符串

    Args:
        length (int, optional): 字符串长度，默认为10.

    Returns:
        str: 生成的随机字符串.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
