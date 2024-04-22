#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/12 15:02:40
@Author  :   ChenHao
@Description  :   测试loader
@Contact :   jerrychen1990@gmail.com
'''
from unittest import TestCase
from loguru import logger
from snippets import set_logger
from xagents.loader.api import load_file
from xagents.config import *
from xagents.loader.common import *


# unit test
class TestEMBD(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start test embd")

    @classmethod
    def show_chunks(cls, chunks:Iterable[Chunk]):
        image_cnt = 0
        for chunk in chunks:
            logger.info(f"page={chunk.page_idx}, type={chunk.content_type}")

            # logger.info(chunk.model_dump_json(indent=4, exclude_none=True, exclude={"data"}))
            if isinstance(chunk, ImageChunk):
                image_cnt += 1
                logger.info(f"image:{chunk.image_name}")
                logger.info(f"content:{chunk.content}")
            if isinstance(chunk, TextChunk):
                logger.info(f"text:{chunk.content}")
    
            if isinstance(chunk, TableChunk):
                logger.info(f"table:\n{chunk.data}")
                logger.info(f"content:\n{chunk.content}")
            logger.info("*"*40+"\n")
        return image_cnt

    def test_load_pdf(self):
        file_path = os.path.join(DATA_DIR, "kb_file", "image_table.pdf")
        chunks = load_file(file_path, end_page=5)
        # image_cnt = 0
        image_cnt = self.show_chunks(chunks)

        self.assertEqual(image_cnt, 4)


    def test_load_docx(self):
        file_path = os.path.join(DATA_DIR, "kb_file", "Xagents中间件.docx")
        chunks = load_file(file_path)
        image_cnt = self.show_chunks(chunks)

        self.assertEqual(image_cnt, 1)