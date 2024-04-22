#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/11 14:22:06
@Author  :   ChenHao
@Description  :   智谱API model的单测
@Contact :   jerrychen1990@gmail.com
'''
import json
import os
from unittest import TestCase
from xagents.model.zhipu import API_GLM
from xagents.model.common import EMBD, LLMResp
from xagents.model import get_embd_model,get_llm_model
from xagents.tool import travel_searcher
from xagents.tool.api import invoke_tool_call
from loguru import logger
from snippets import set_logger


# unit test
class TestEMBD(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start test embd")
        cls.zhipu_api_embedding:EMBD= get_embd_model(dict(cls="ZhipuEmbedding", api_key=os.environ["ZHIPU_API_KEY"], batch_size=4))

    def test_zhipu_api(self):
        # set_logger("dev", "")
        texts = ["你好", "hello"]
        embds = self.zhipu_api_embedding.embed_documents(texts)
        logger.info(len(embds))
        self.assertEqual(len(embds), 2)
        import numpy as np
        logger.info(np.linalg.norm(embds[0]))
        self.assertAlmostEqual(np.linalg.norm(embds[0]), 1.0)

        print(embds[0][:4])
        embd = self.zhipu_api_embedding.embed_query(text=texts[0])
        print(embd[:4])
        self.assertListEqual(embds[0], embd)
        
class TestGLM(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start llm")
        cls.zhipu_api_llm_model:API_GLM = get_llm_model(dict(cls="GLM", api_key=os.environ["ZHIPU_API_KEY"], name="glm-3-turbo", version="glm-3-turbo" ))

    def test_zhipu_api(self):
        # set_logger("dev", "")
        prompt = "你好呀，你是谁"
        _system = "请用英语回答我的问题，你的名字叫XAgent"
        
        # 测试zhipu api
        resp:LLMResp = self.zhipu_api_llm_model.generate(prompt=prompt, system=_system, temperature=0.7, top_p=0.95, max_tokens=100, log_level="INFO", stream=False)        

        logger.info(json.dumps(resp.model_dump(), ensure_ascii=False, indent=4))
        self.assertIsNotNone(resp.content)        
        self.assertIsNotNone(resp.usage)        


        ## 流式
        resp:LLMResp = self.zhipu_api_llm_model.generate(prompt=prompt, system=_system, temperature=0.7, top_p=0.95, max_tokens=100, log_level="INFO", stream=True)        
        for chunk in resp.content:
            logger.info(chunk)
        logger.info(json.dumps(resp.model_dump(exclude={"content"}), ensure_ascii=False, indent=4))
        self.assertIsNotNone(resp.usage)

  
    def test_zhipu_api_tool_call(self):   


        prompt = "你能帮我查询2024年1月1日从北京南站到上海的火车票吗？"
        _system = None
        tools = [travel_searcher]
        # 测试zhipu api
        resp:LLMResp = self.zhipu_api_llm_model.generate(prompt=prompt, system=_system, tools=tools, temperature=0.7, top_p=0.95, max_tokens=100, log_level="INFO", stream=False)        
        logger.info(json.dumps(resp.model_dump(), ensure_ascii=False, indent=4))
        self.assertIsNotNone(resp.tool_calls)        
        self.assertIsNotNone(resp.usage)       
        #调用工具
        logger.info("invoking tools")
        for tool_call in resp.tool_calls:        
            tool_resp = invoke_tool_call(tool_call)
                        

            tool_call.resp=tool_resp
            resp:LLMResp = self.zhipu_api_llm_model.observe(prompt=prompt, tool_call=tool_call, tools=tools, stream=False)
            
            logger.info(json.dumps(resp.model_dump(), ensure_ascii=False, indent=4))
            self.assertIsNotNone(resp.content)        
            self.assertIsNotNone(resp.usage)  
        
         


        # ## 流式
        resp = self.zhipu_api_llm_model.generate(prompt=prompt, system=_system, tools=tools, temperature=0.7, top_p=0.95, max_tokens=100, log_level="INFO", stream=False)
        logger.info(json.dumps(resp.model_dump(exclude={"content"}), ensure_ascii=False, indent=4))

        self.assertIsNotNone(resp.tool_calls)        
        self.assertIsNotNone(resp.usage)
        
        #调用工具
        logger.info("invoking tools")
        for tool_call in resp.tool_calls:        
            tool_resp = invoke_tool_call(tool_call)
                    
            tool_call.resp=tool_resp
            resp:LLMResp = self.zhipu_api_llm_model.observe(prompt=prompt, tool_call=tool_call, tools=tools, stream=True)
            for chunk in resp.content:
                logger.info(chunk)
            logger.info(json.dumps(resp.model_dump(exclude={"content"}), ensure_ascii=False, indent=4))
            self.assertIsNotNone(resp.usage)
