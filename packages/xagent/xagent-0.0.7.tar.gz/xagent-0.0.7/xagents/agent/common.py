#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/07 17:54:34
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

from typing import List, Optional

from abc import abstractmethod

from pydantic import BaseModel, Field

from agit.common import LLMResp
from xagents.config import DEFAULT_KB_PROMPT_TEMPLATE, DEFAULT_WEB_SEARCH_KB_PROMPT_TEMPLATE, \
    DEFAULT_WEB_SEARCH_PROMPT_TEMPLATE
from xagents.kb.common import RecalledChunk

# class WebResult(BaseModel):
#     summary:str
#     pages:List[str, str]


class WebPage(BaseModel):
    url:str = Field(description="网页的URL")
    content:str = Field(description="网页的内容")    

class WebSearchResp(BaseModel):
    summary: str = Field(description="搜索结果的摘要")
    pages: List[WebPage]|None = Field(description="搜索结果的网页列表")
    

class AgentResp(LLMResp):
    references: Optional[List[RecalledChunk]] = Field(description="召回的片段")
    web_search_result: Optional[WebSearchResp] = Field(description="联网搜索的结果", default=None)
    
class AbstractAgent:

    def __init__(self, name) -> None:
        self.name = name

    @abstractmethod
    def chat(self, message: str, stream=True, do_remember=True) -> AgentResp:
        raise NotImplementedError

    @abstractmethod
    def remember(self, role: str, message: str):
        raise NotImplementedError


class KBConfig(BaseModel):
    name: str = Field(description="知识库名称")
    prompt_template: str = Field(description="应用知识库的提示词模板, 必须包含{context}和{question}两个字段",
                                 default=DEFAULT_KB_PROMPT_TEMPLATE)


class WebSearchConfig(BaseModel):
    name: str = Field(description="应用联网搜索的名称")
    prompt_search_template: str = Field(
        description="应用联网搜索的提示词模板, 必须包含{seach_info}和{question}两个字段",
        default=DEFAULT_WEB_SEARCH_PROMPT_TEMPLATE)
    prompt_search_kb_template: str = Field(
        description="应用知识库的提示词模板, 必须包含{search_info},{context}和{question}三个字段",
        default=DEFAULT_WEB_SEARCH_KB_PROMPT_TEMPLATE)
