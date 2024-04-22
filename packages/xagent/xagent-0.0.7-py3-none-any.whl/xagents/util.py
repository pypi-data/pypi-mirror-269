#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/03/15 16:00:04
@Author  :   ChenHao
@Description  :   工具包
@Contact :   jerrychen1990@gmail.com
'''


from functools import wraps
from typing import Callable

from fastapi.params import Body

from loguru import logger


def parse_body(func:Callable):
    @wraps(func)
    def wrapped(**kwargs):
        print(f"{kwargs=}")
        for k,v in kwargs.items():
            if isinstance(v, Body):
                kwargs[k] = v.default
        return func(**kwargs)
    return wrapped




