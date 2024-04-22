#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/11 17:17:19
@Author  :   ChenHao
@Description  :   测试xagent
@Contact :   jerrychen1990@gmail.com
'''

from unittest import TestCase
import sys
# sys.path.append("../")
from xagents.agent.api import *
from xagents.kb.api import *
from loguru import logger
from snippets import set_logger


# unit test
class TestXagent(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start test embd")

    def test_agent_tool_use(self):
        agent_name = "unittest_agent"
        llm_config = dict(cls="GLM", version="glm-3-turbo")
        tools_config = [dict(name="计算器"), dict(name="车次查询")]

        # create agent
        agent: XAgent = create_agent(name=agent_name, llm_config=llm_config, tools_config=tools_config)
        logger.info(f"create Agent {agent.get_info()} success")

        # chat with agent
        message = "你能帮我查询2024年1月1日从北京南站到上海的火车票吗？"

        llm_gen_config = LLMGenConfig()
        agent_resp = chat_agent(name=agent.name, message=message, stream=True, llm_gen_config=llm_gen_config)
        logger.info(f"agent resp: {agent_resp.model_dump(exclude={'content'})}")
        self.assertIsNotNone(agent_resp.content)
        for chunk in agent_resp.content:
            logger.info(chunk)
        self.assertIsNotNone(agent_resp.usage)

    def test_agent_tool_websearch_use(self):

        agent_name = "unittest_agent"
        llm_config = dict(cls="GLM", version="glm-3-turbo")
        kb_name = "unittest_kb"
        self._init_kb(kb_name)
        kb_config = KBConfig(name=kb_name)
        tools_config = [dict(name="联网查询")]
        #
        # web_search_config = WebSearchConfig(name = "test")
        # print(f"web_search_config1:{web_search_config}")

        logger.info(f"create tools_config_v1 {tools_config} success")
        # create agent
        agent: XAgent = create_agent(name=agent_name, llm_config=llm_config, tools_config=tools_config, kb_config=kb_config)
        logger.info(f"create Agent {agent.get_info()} success")

        # chat with agent
        message = "帮我查询一下杭州的最新天气"#"你能帮我找一下今天关于杭州实时新闻吗？"
        kb_search_config = KBSearchConfig(do_expand=True, expand_len=200)
        llm_gen_config = LLMGenConfig()
        agent_resp = chat_agent(name=agent.name, message=message, use_kb = False, stream=False, kb_search_config= kb_search_config, llm_gen_config=llm_gen_config)
        logger.info(f"agent resp: {agent_resp.model_dump()}")
        self.assertIsNotNone(agent_resp.content)
        self.assertIsNotNone(agent_resp.usage)

    def test_agent_multi_turn(self):
        agent_name = "unittest_agent"
        llm_config = dict(cls="GLM", version="glm-3-turbo")
        _system = "请用英语回答我的问题"

        # create agent
        agent: XAgent = create_agent(name=agent_name, llm_config=llm_config)
        logger.info(f"create Agent {agent.get_info()} success")

        # chat with agent
        message = "帮我推荐三首歌"
        llm_gen_config = LLMGenConfig(system=_system)
        agent_resp = chat_agent(name=agent.name, message=message, stream=True, llm_gen_config=llm_gen_config)
        # agent_resp = agent.chat(name=agent.name, message=message, llm_gen_config=llm_gen_config)

        self.assertIsNotNone(agent_resp.content)
        content = "".join(agent_resp.content)
        logger.info(content)
        logger.info(f"agent resp: {agent_resp.model_dump(exclude={'content'})}")

        self.assertIsNotNone(agent_resp.usage)

        # logger.debug(f"agent_memory:{agent.memory.to_llm_history()}")

        message = "详细介绍一下第三首"
        llm_gen_config = LLMGenConfig(system=_system)

        agent_resp = chat_agent(name=agent.name, message=message, stream=False, llm_gen_config=llm_gen_config, details=True)
        # agent_resp = agent.chat(name=agent.name, message=message, llm_gen_config=llm_gen_config,details=True)

        self.assertIsNotNone(agent_resp.content)
        logger.info(f"agent resp: {agent_resp.model_dump()}")

        self.assertIsNotNone(agent_resp.usage)
        self.assertNotEquals(len(agent_resp.details), 0)

    def _init_kb(self, kb_name: str):
        try:
            kb = get_knowledge_base(kb_name)
        except Exception as e:
            kb = create_knowledge_base(kb_name)
        file_name = "README.md"
        try:
            kb_file = get_kb_file_info(kb_name=kb_name, file_name=file_name)
        except Exception as e:
            cur_dir = os.path.abspath(os.path.dirname(__file__))
            file_path = os.path.join(os.path.dirname(cur_dir), file_name)
            logger.debug(f"adding file:{file_path}")
            kb_file = create_kb_file(kb_name=kb_name, file=file_path)

    def test_agent_kb(self):
        agent_name = "unittest_agent"
        llm_config = dict(cls="GLM", version="glm-3-turbo")
        kb_name = "unittest_kb"
        self._init_kb(kb_name)
        kb_config = KBConfig(name=kb_name)

        # create agent
        agent: XAgent = create_agent(name=agent_name, llm_config=llm_config, kb_config=kb_config)
        logger.info(f"create Agent {agent.get_info()} success")

        # chat with agent
        message = "20240401发布了哪些功能？"
        llm_gen_config = LLMGenConfig()
        kb_search_config = KBSearchConfig(do_expand=True, expand_len=200)
        agent_resp = chat_agent(name=agent.name, message=message, use_kb=True, stream=False, kb_search_config=kb_search_config, llm_gen_config=llm_gen_config)
        # agent_resp = agent.chat(name=agent.name, message=message, llm_gen_config=llm_gen_config)

        self.assertIsNotNone(agent_resp.content)
        content = "".join(agent_resp.content)
        logger.info(f"agent resp:{content}")

        self.assertIsNotNone(agent_resp.references)
        for reference in agent_resp.references:
            logger.info(f"reference: {reference.to_plain_text()}")

        self.assertIsNotNone(agent_resp.usage)

        logger.info(f"agent resp: {agent_resp.model_dump(exclude={'content'})}")



