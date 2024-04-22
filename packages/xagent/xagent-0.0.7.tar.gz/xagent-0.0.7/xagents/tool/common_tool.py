#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/01/04 14:04:02
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''
import sys
from xagents.tool.core import BaseTool
from agit.common import Parameter


def exec_python(expression: str) -> dict:
    try:
        rs = eval(expression)
    except Exception as e:
        rs = "执行失败"
    return dict(result=rs)


def mock_travel_search(departure: str, destination: str, date: str):
    return dict(result="查询成功，有如下车次:A00001, A00002, A00003")


calculator = BaseTool(name="计算器", description="根据提供的数学表达式，用python解释器来执行，得到计算结果,计算结果以json格式来返回,json包含一个字段，名字为result",
                      parameters=[Parameter(name="expression", type="string", description="数学表达式，可以通过python来执行的", required=True)],
                      callable=exec_python)

travel_searcher = BaseTool(name="车次查询", description="根据用户提供的信息，查询对应的车次",
                           parameters=[Parameter(name="departure", description="出发城市或车站", type="string", required=True),
                                       Parameter(name="destination", description="目的地城市或车站", type="string", required=True),
                                       Parameter(name="date", description="要查询的车次日期", type="string", required=True)],
                           callable=mock_travel_search)


if __name__ == "__main__":
    rs = calculator.execute("(351345-54351)/54351")
    print(rs)
