#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/01/04 14:01:01
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

from typing import Any, Callable

from pydantic import Field
from agit.common import ToolDesc, ToolCall, ToolDesc



class BaseTool(ToolDesc):
    callable:Callable = Field(..., description="工具执行函数")
    
    
    def execute(self, *args, **kwargs) -> Any:
        return self.callable(*args, **kwargs)
