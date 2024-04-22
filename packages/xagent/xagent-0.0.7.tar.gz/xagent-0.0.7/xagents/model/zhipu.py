#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/07 17:47:22
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

from typing import List
import requests
from xagents.model.common import LLM, EMBD, Reranker
# from agit.backend.zhipuai_bk import call_llm_api
from agit.llm import call_llm, LLMResp
from agit.common import ToolCall
from agit.embd import call_embedding, EMBD_TYPE

from xagents.tool.core import ToolCall
from xagents.tool import BaseTool

from loguru import logger


class API_GLM(LLM):
    def __init__(self, version: str, name: str = None,  api_key=None):
        assert version in self.list_versions(), f"{version} not in {self.list_versions()}"
        super().__init__(name=name, version=version)
        self.api_key = api_key

    @classmethod
    def list_versions(cls):
        return [
            "glm-4",
            "glm-3-turbo",
            "chatglm3_130b",
            "chatglm_turbo",
            "chatglm_pro",
            "chatglm_66b",
            "chatglm_12b",
            "chatglm2_12b_32k"
        ]

    def observe(self, prompt: str, tool_call: ToolCall,  tools: List[BaseTool] = [], history=[], stream=True, **kwargs):
        observe_message = dict(role="tool", content=str(tool_call.resp), tool_call_id=tool_call.tool_call_id)
        messages = history + [dict(role="user", content=prompt)] + [observe_message]

        resp = call_llm(messages=messages, tools=tools,  model=self.version, do_search=False, stream=stream, api_key=self.api_key, **kwargs)
        logger.debug(f"observe result:{resp}")
        return resp

    def generate(self, prompt, history=[], system=None, tools: List[BaseTool] = [], stream=True, **kwargs) -> LLMResp:
        # logger.info(f"{self.__class__} generating resp with {prompt=}, {history=}")
        messages = history + [dict(role="user", content=prompt)]
        resp: LLMResp = call_llm(messages=messages, model=self.version, tools=tools, do_search=False,
                                 system=system, stream=stream, api_key=self.api_key, **kwargs)
        return resp


class ZhipuEmbedding(EMBD):
    def __init__(self,  api_key=None, batch_size=16, norm=True):
        self.api_key = api_key
        self.batch_size = batch_size
        self.norm = norm

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = call_embedding(text=texts, embd_type=EMBD_TYPE.ZHIPU_API, model_or_url="embedding-2",
                                    norm=self.norm, batch_size=self.batch_size)
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        embedding = call_embedding(text=text, embd_type=EMBD_TYPE.ZHIPU_API, model_or_url="embedding-2",
                                   norm=self.norm, batch_size=self.batch_size)
        return embedding

    @classmethod
    def get_dim(cls) -> int:
        return 1024


class ZhipuReranker(Reranker):
    def __init__(self,  url: str, name="reranker", version="ZhipuReranker"):
        self.url = url
        super().__init__(name=name, version=version)

    def cal_similarity(self, text1: str, text2: str):
        logger.debug(f"rerank simi for {text1}, {text2}")
        resp = requests.post(url=self.url, params=dict(text1=text1, text2=text2))
        resp.raise_for_status()
        return resp.json()["data"]["score"]


if __name__ == "__main__":
    # llm_model = GLM(name="glm", version="chatglm_turbo")
    # resp = llm_model.generate("你好", stream=False)
    # print(resp)

    # embd_model = ZhipuEmbedding()
    # text = ["中国", "美国", "日本", "法国", "英国", "意大利", "西班牙", "德国", "俄罗斯"]
    # embds = embd_model.embed_documents(text)
    # print(len(embds))
    # print(embds[0][:4])
    # embd = embd_model.embed_query("你好")
    # print(len(embd))
    # print(embd[:4])

    reranker = ZhipuReranker(url="http://hz-model.bigmodel.cn/reranker/get_rel_score", name="zhipu_ranker", version="bge-reranker-base")
    sim = reranker.cal_similarity("私募基金", "公募基金")
    print(sim)
