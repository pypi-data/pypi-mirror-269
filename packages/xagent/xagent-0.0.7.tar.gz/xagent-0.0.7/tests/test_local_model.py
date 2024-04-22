#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/11 14:22:06
@Author  :   ChenHao
@Description  :   智谱API model的单测
@Contact :   jerrychen1990@gmail.com
'''
import json
from unittest import TestCase
from xagents.model.api import get_llm_model
from xagents.model.common import EMBD, LLM, LLMResp
from xagents.model import get_embd_model
from loguru import logger
from snippets import set_logger
from agit.utils import cal_vec_similarity


# unit test
class TestEMBD(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start test embd")
        cls.local_embd:EMBD= get_embd_model(dict(cls="LocalEmbedding", batch_size=4, norm=False))

    def test_local_embd(self):
        # set_logger("dev", "")
        texts = ["你好", "hello"]
        embds = self.local_embd.embed_documents(texts)
        logger.info(len(embds))
        self.assertEqual(len(embds), 2)
        self.assertEqual(len(embds[0]), self.local_embd.get_dim())
        import numpy as np
        logger.info(np.linalg.norm(embds[0]))
        self.assertNotEqual(np.linalg.norm(embds[0]), 1.0)

        print(embds[0][:4])
        embd = self.local_embd.embed_query(text=texts[0])
        print(embd[:4])
        
        cosine_simi = cal_vec_similarity(embds[0], embd)
        logger.info(f"cosine similarity: {cosine_simi}")
        self.assertAlmostEquals(cosine_simi, 1.)    
            
class TestTGI(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start llm")
        cls.tgi_llm_model:LLM = get_llm_model(dict(cls="TGI_GLM", url="http://hz-model.bigmodel.cn/wind-130b"))

    def test_zhipu_api(self):
        # set_logger("dev", "")
        prompt = "你好呀，你是谁"
        _system = "请用英语回答我的问题，你的名字叫XAgent"
        
        # 测试zhipu api
        resp:LLMResp = self.tgi_llm_model.generate(prompt=prompt, system=_system, temperature=0.7, top_p=0.95, max_tokens=100, log_level="INFO", stream=False)        

        logger.info(json.dumps(resp.model_dump(), ensure_ascii=False, indent=4))
        self.assertIsNotNone(resp.content)        


        ## 流式
        resp:LLMResp = self.tgi_llm_model.generate(prompt=prompt, system=_system, temperature=0.7, top_p=0.95, max_tokens=100, log_level="INFO", stream=True)        
        for chunk in resp.content:
            logger.info(chunk)
        logger.info(json.dumps(resp.model_dump(exclude={"content"}), ensure_ascii=False, indent=4))

  