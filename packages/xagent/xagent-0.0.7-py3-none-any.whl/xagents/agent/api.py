#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/01 13:46:25
@Author  :   ChenHao
@Description  :   Agent问答的api
@Contact :   jerrychen1990@gmail.com
'''
from enum import Enum
from typing import List
from xagents.tool.api import get_tools
from xagents.model.common import LLMGenConfig
from xagents.kb.api import KBSearchConfig
from xagents.config import AGENT_DIR, XAGENT_CACHE_NUM
from xagents.agent.common import AgentResp, KBConfig, WebSearchConfig
from xagents.agent.xagent import XAgent
from cachetools import LRUCache, cached
from loguru import logger

agent_cache = LRUCache(maxsize=XAGENT_CACHE_NUM)


class STORE_TYPE(str, Enum):
    CACHE = "CACHE"
    DISK = "DISK"


def create_agent(name: str, llm_config: dict = dict(cls="GLM", name="glm", version="glm-4"),
                 tools_config: List[dict] = [], memory_config: dict = dict(size=10),
                 kb_config: KBConfig = None, store_type=STORE_TYPE.CACHE) -> XAgent:

    logger.info(f"creating agent:{name}")
    # print(f"web_search_config2:{web_search_config}")

    @cached(agent_cache)
    def _get_or_create(name: str):
        tools = get_tools( tools_config)  #  [{'name': '联网查询'}]
        # print(f"web_search_config3:{web_search_config}")
        logger.info(f"getting tools_config:{tools_config}")
        logger.info(f"getting tools:{tools}")
        xagent = XAgent(name=name, llm_config=llm_config, memory_config=memory_config, kb_config=kb_config, tools=tools)
        return xagent
    agent = _get_or_create(name=name)
    if store_type == STORE_TYPE.DISK:
        agent.save(AGENT_DIR)
        
    return agent


@cached(agent_cache)
def get_agent(name: str) -> XAgent:
    agent = XAgent.load(AGENT_DIR, name)
    return agent    


def chat_agent(name: str, message: str, do_remember=True, details=False, stream=False,
               use_kb=False, kb_search_config:KBSearchConfig=KBSearchConfig(),
               fake_chat=False, llm_gen_config:LLMGenConfig = LLMGenConfig()) -> AgentResp:
    """和Agent对话

    Args:
        name (str): Agent的名称
        message (str): 用户发送的消息
        do_remember (bool, optional): Agent是否要记住历史对话. Defaults to True.
        details (bool, optional): 是否返回详细调用信息. Defaults to False.
        use_kb (bool, optional): 是否使用知识库. Defaults to False.
        kb_search_config (KBSearchConfig, optional): 知识库查询参数，use_kb=True时生效. Defaults to KBSearchConfig().
        fake_chat (bool, optional): 是否fake大模型问答（fake_chat=True时，不会调用LLM）. Defaults to False.
        llm_gen_config (LLMGenConfig, optional): 大模型生成文本需要的参数. Defaults to LLMGenConfig.

    Returns:
        AgentResp: Agent回答的结构体
    """
    # logger.info(f"sending message:{message} to agent:{name}")
    agent = get_agent(name=name)
    agent_resp = agent.chat(message=message, do_remember=do_remember, details=details, stream=stream,
                            use_kb=use_kb, kb_search_config=kb_search_config,
                            fake_chat=fake_chat, llm_gen_config=llm_gen_config)
    return agent_resp


def clear_agent(name:str) ->None:
    """清空agent的历史对话记录

    Args:
        name (str): agent的名称
    """
    logger.info(f"clear memory of {name}")
    agent = get_agent(name=name)
    agent.clear_memory()
