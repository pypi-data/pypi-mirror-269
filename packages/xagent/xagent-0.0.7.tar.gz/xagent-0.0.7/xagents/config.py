#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/07 18:40:00
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''
import os

XAGENT_ENV = os.environ.get("XAGENT_ENV", "dev")
XAGENT_HOME = os.path.dirname(os.path.dirname(__file__))

KNOWLEDGE_BASE_DIR = os.environ.get("XAGENT_KNOWLEDGE_BASE_DIR", os.path.join(XAGENT_HOME, "knowledge_base"))
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)

TEMP_DIR = os.environ.get("XAGENT_TEMP_DIR", os.path.join(XAGENT_HOME, "tmp"))
os.makedirs(TEMP_DIR, exist_ok=True)

LOG_DIR = os.environ.get("XAGENT_LOG_DIR", os.path.join(XAGENT_HOME, "log"))
os.makedirs(LOG_DIR, exist_ok=True)

DB_DIR = os.environ.get("XAGENT_DB_DIR", os.path.join(XAGENT_HOME, "db"))
os.makedirs(DB_DIR, exist_ok=True)

AGENT_DIR = os.environ.get("XAGENT_AGENT_DIR", os.path.join(XAGENT_HOME, "agent"))
os.makedirs(AGENT_DIR, exist_ok=True)

DATA_DIR = os.path.join(XAGENT_HOME, "data")


DEFAULT_KB_PROMPT_TEMPLATE = '''请根据[参考信息]回答我的问题，如果问题不在参考信息内，请不要参考
[参考信息]
{context}

问题:
{question}
'''

DEFAULT_WEB_SEARCH_PROMPT_TEMPLATE = '''请根据[搜索信息]回答我的问题，如果问题不在搜索信息内，请不要参考
[搜索信息]
{search_info}
问题:
{question}
'''

DEFAULT_WEB_SEARCH_KB_PROMPT_TEMPLATE = '''请根据[参考信息]和[搜索信息]回答我的问题，如果问题不在参考信息和搜索信息内，请不要参考
[参考信息]
{context}
[搜索信息]
{search_info}
问题:
{question}
'''


### Service相关
### 最大job数（job用来处理知识库index任务）
MAX_JOB_NUM=10
### 用户鉴权配置
USERNAME="zhipu"
PASSWORD="zhipu"
### xagent缓存数目
XAGENT_CACHE_NUM=1000
XAGENT_CACHE_EXPIRE_SECONDS=3600