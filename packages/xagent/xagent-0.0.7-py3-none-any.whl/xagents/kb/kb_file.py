#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/03/19 16:10:35
@Author  :   ChenHao
@Description  :  知识库文件类
@Contact :   jerrychen1990@gmail.com
'''


# 知识库文件类
import os
from loguru import logger
from typing import List
from xagents.kb.common import KBChunk, KnowledgeBaseFileInfo, get_chunk_path, get_id_path, get_origin_path
from xagents.loader.api import parse_file
from xagents.loader.common import Chunk
from snippets import dump, load


class KnowledgeBaseFile:
    def __init__(self, kb_name: str, file_name: str):
        self.kb_name = kb_name
        self.file_name = file_name

        self.chunk_path = get_chunk_path(self.kb_name, self.file_name)
        self.origin_path = get_origin_path(self.kb_name, self.file_name)
        self.id_path = get_id_path(self.kb_name, self.file_name)

    @property
    def is_cut(self) -> bool:
        return os.path.exists(self.chunk_path)

    @property
    def is_indexed(self) -> bool:
        return os.path.exists(self.id_path)

    @property
    def chunk_num(self) -> int:
        if not self.is_cut:
            return 0
        chunks = load(self.chunk_path)
        return len(chunks)

    def get_info(self):
        return KnowledgeBaseFileInfo(kb_name=self.kb_name, file_name=self.file_name, is_cut=self.is_cut, is_indexed=self.is_indexed)

    def cut(self, *args, **kwargs):
        logger.info(f"start cut file: {self.file_name}")
        chunks: List[Chunk] = parse_file(file_path=self.origin_path, *args, **kwargs)
        kb_chunks = [KBChunk(**chunk.to_json(), idx=idx, kb_name=self.kb_name, file_name=self.file_name)
                     for idx, chunk in enumerate(chunks) if chunk.content]
        kb_chunk_json = [chunk.to_dict() for chunk in kb_chunks]
        dump(kb_chunk_json, self.chunk_path)
        return len(kb_chunks)

    def get_chunks(self) -> List[KBChunk]:
        """
        从切片文件加载切片
        """
        if not self.is_cut:
            return []

        chunk_dicts = load(self.chunk_path)
        logger.debug(f"loaded {len(chunk_dicts)} chunks from {self.chunk_path}")
        chunks: List[KBChunk] = [KBChunk(**c, idx=idx, kb_name=self.kb_name, file_name=self.file_name) for idx, c in enumerate(chunk_dicts)]
        return chunks

    def remove(self):
        """
        删除知识库文档
        """
        for path in [self.origin_path, self.chunk_path]:
            if os.path.exists(path):
                os.remove(path)
