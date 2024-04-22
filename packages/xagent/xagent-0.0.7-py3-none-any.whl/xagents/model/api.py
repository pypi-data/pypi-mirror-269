#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/12 15:50:25
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''
import copy
from typing import List
from loguru import logger
from xagents.model.common import LLM, EMBD, Reranker
from xagents.model.zhipu import ZhipuReranker, ZhipuEmbedding, API_GLM
from xagents.model.local import LocalEmbedding, TGI_GLM


_LLM_MODELS = [API_GLM, TGI_GLM]
_LLM_MODELS_DICT = {model.__name__: model for model in _LLM_MODELS}

## 向前兼容
_LLM_MODELS_DICT.update(GLM=API_GLM)


_EMBD_MODELS = [ZhipuEmbedding, LocalEmbedding]
_EMBD_MODELS_DICT = {model.__name__: model for model in _EMBD_MODELS}

_RERANK_MODELS = [ZhipuReranker]
_RERANK_MODELS_DICT = {model.__name__: model for model in _RERANK_MODELS}


def list_llm_models() -> List[str]:
    return [e.__name__ for e in _LLM_MODELS]


def list_embd_models() -> List[str]:
    return [e.__name__ for e in _EMBD_MODELS]


def list_llm_versions(llm_model: str) -> List[str]:
    model_cls = _LLM_MODELS_DICT[llm_model]
    return model_cls.list_versions()


def get_llm_model(config: dict) -> LLM:
    tmp_config = copy.copy(config)
    model_cls = tmp_config.pop("cls")
    if model_cls not in _LLM_MODELS_DICT:
        msg = f"unknown LLM model: {model_cls}, valid keys:{_LLM_MODELS_DICT.keys()}"
        raise ValueError(msg)
    model_cls = _LLM_MODELS_DICT[model_cls]
    return model_cls(**tmp_config)


def get_embd_model(config: dict) -> EMBD:
    logger.debug(f"get_embd_model with config:{config}")
    tmp_config = copy.copy(config)
    model_cls = tmp_config.pop("cls")
    if model_cls not in _EMBD_MODELS_DICT:
        msg = f"unknown embedding model: {model_cls}, valid keys:{_EMBD_MODELS_DICT.keys()}"
        raise ValueError(msg)
    model_cls = _EMBD_MODELS_DICT[model_cls]
    return model_cls(**tmp_config)

def get_rerank_model(config:dict)->Reranker:
    if not config:
        return None
    tmp_config = copy.copy(config)
    model_cls = tmp_config.pop("cls")
    model_cls = _RERANK_MODELS_DICT[model_cls]
    return model_cls(**tmp_config)
    


if __name__ == "__main__":
    # config = dict(model_cls="GLM", name="glm", version="chatglm_turbo")
    # model = get_llm_model(config)
    # resp = model.generate(prompt="你好", stream=False)
    # print(resp)
    # rerank_config = dict(model_cls="ZhipuReranker", url="http://hz-model.bigmodel.cn/reranker/get_rel_score")
    # rerank_model = get_rerank_model(rerank_config)
    # score = rerank_model.cal_similarity("你好","你滚")
    # print(score)
    embedding_model_list = list_embd_models()
    print(embedding_model_list)
    embedding_model_config = dict(cls='ZhipuLocalEmbedding')
    cur_embedding_model = get_embd_model(embedding_model_config)
    print(cur_embedding_model)
    
    
