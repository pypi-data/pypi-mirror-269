#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/02/20 15:47:53
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


from typing import List


import requests
from snippets import *
from xagents.model.common import LLM, EMBD
from agit.llm import LLM_TYPE, call_llm, LLMResp
from agit.embd import EMBD_TYPE, call_embedding

from loguru import logger


def call_local_embedding(url: str, contents: List[str], norm=True) -> List[List[float]]:
    # embeddings = []
    # url = "http://36.103.177.140:8001/v2/embeddings"
    resp = requests.post(url=url, json=dict(texts=contents, norm=norm))
    resp.raise_for_status()
    return resp.json()["data"]['embeddings']


class LocalEmbedding(EMBD):

    def __init__(self,  url="http://hz-model.bigmodel.cn/embedding-models/v2/embeddings", batch_size=16, norm=True):
        self.batch_size = batch_size
        self.norm = norm
        self.url = url

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        logger.info(f"embedding {len(texts)} with {self.batch_size=}")
        embeddings = call_embedding(text=texts,model_or_url=self.url, embd_type=EMBD_TYPE.LOCAL,
                                    norm=self.norm, batch_size=self.batch_size)
        
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        embedding = call_embedding(text=text,model_or_url=self.url, embd_type=EMBD_TYPE.LOCAL,
                                    norm=self.norm, batch_size=self.batch_size)
        return embedding

    @classmethod
    def get_dim(cls) -> int:
        return 1024


class TGI_GLM(LLM):
    """
    本地调用LLM
    """

    @classmethod
    def list_versions(cls):
        return [
            "v1.0.0",
        ]

    def __init__(self, url:str, name=None, version="v1.0.0"):
        super().__init__(name=name, version=version)
        self.url = url

    def generate(self, prompt:str, history=[], system:str=None, stream=True, **kwargs)->LLMResp:
        messages = history + [{"role": "user", "content": prompt}]
        resp = call_llm(messages=messages, url=self.url, llm_type=LLM_TYPE.TGI, system=system,
                        stream=stream, **kwargs)

        return resp
