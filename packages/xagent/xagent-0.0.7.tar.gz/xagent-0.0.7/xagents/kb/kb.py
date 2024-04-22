#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/03/19 15:45:46
@Author  :   ChenHao
@Description  :   
@Contact :   jerrychen1990@gmail.com
'''
import copy
import os
import re
from typing import List, Type
from loguru import logger
from xagents.kb.kb_file import KnowledgeBaseFile
from xagents.kb.vector_store import LocalVecStore, XVecStore, get_vecstore_cls
from xagents.loader.common import Chunk
from xagents.model.api import get_embd_model, get_rerank_model
from xagents.kb.common import KnowledgeBaseInfo, RecalledChunk, get_chunk_dir, get_chunk_path, get_config_path, get_id_dir, get_index_dir, get_kb_dir, get_origin_dir, DistanceStrategy
from snippets import load, log_cost_time, dump


class KnowledgeBase():

    def __init__(self, name: str, desc, embedding_config: dict, vecstore_config: dict):
        self.name = name
        self.desc = desc
        self.embedding_config = embedding_config
        self.vecstore_config = vecstore_config
        self._build_dirs()
        self._save_config()
        self.index=None

    @classmethod
    def from_config(cls, config: dict | str):
        if isinstance(config, str):
            config = load(config)
        return cls(**config)

    def _get_config(self) -> dict:
        return dict(name=self.name, desc=self.desc, embedding_config=self.embedding_config, vecstore_config=self.vecstore_config)

    def get_info(self) -> KnowledgeBaseInfo:
        """返回知识库的信息

        Returns:
            dict: 知识库信息
        """
        file_num = len(list(self.list_kb_files()))
        return KnowledgeBaseInfo(**self._get_config(), file_num=file_num)

    def _build_dirs(self):
        self.kb_dir = get_kb_dir(self.name)
        self.origin_dir = get_origin_dir(self.name)

        self.chunk_dir = get_chunk_dir(self.name)
        self.index_dir = get_index_dir(self.name)
        self.id_dir = get_id_dir(self.name)
        self.config_path = get_config_path(self.name)

        os.makedirs(self.origin_dir, exist_ok=True)
        os.makedirs(self.chunk_dir, exist_ok=True)
        os.makedirs(self.id_dir, exist_ok=True)

    def _save_config(self):
        dump(self._get_config(), self.config_path)

    def get_index(self) -> XVecStore:
        """
        加载向量库
        """
        if not self.index:
            config = copy.copy(self.vecstore_config)
            vecstore_cls: Type[XVecStore] = get_vecstore_cls(config.pop("cls"))
            embedding_model = get_embd_model(self.embedding_config)
            config.update(embedding=embedding_model, local_dir=self.index_dir)
            self.index = vecstore_cls.from_config(config)
        return self.index

    def list_kb_files(self) -> List[KnowledgeBaseFile]:
        kb_files = []
        for file_name in os.listdir(self.origin_dir):
            kb_file = KnowledgeBaseFile(kb_name=self.name, file_name=file_name)
            kb_files.append(kb_file)
        return kb_files

    def remove_file(self, kb_file: KnowledgeBaseFile):
        """
        删除文档
        """
        assert kb_file.kb_name == self.name
        kb_file.remove()
        if kb_file.is_indexed:
            index = self.get_index()
            logger.debug(f"{index=}")
            self.remove_kb_file_from_index(index, kb_file)

    def remove_kb_file_from_index(self, index: XVecStore, kb_file: KnowledgeBaseFile):
        if kb_file.is_indexed:
            doc_ids = load(kb_file.id_path)
            index.delete(doc_ids)
            os.remove(kb_file.id_path)

    def add_kb_file2index(self, index: XVecStore, kb_file: KnowledgeBaseFile, reindex=False, do_save=False, batch_size=16):
        if not kb_file.is_cut:
            logger.warning(f"{kb_file.file_name} is not cut, please cut it first")
            return

        if kb_file.is_indexed and not reindex:
            logger.info(f"{kb_file.file_name} is already indexed, skip")
        else:

            embd_model = index.embeddings
            if hasattr(embd_model, "batch_size"):
                logger.debug(f"setting embedding model batch size to {batch_size}")
                setattr(embd_model, "batch_size", batch_size)
            else:
                logger.warning(f"{embd_model.__class__} has no attribute batch_size, set to default value {batch_size}")  
                
            self.remove_kb_file_from_index(index, kb_file)
            chunks = kb_file.get_chunks()
            documents = [chunk.to_document() for chunk in chunks if chunk.content]

            logger.info(f"reindexing {kb_file.file_name} with {len(chunks)}chunks and {len(documents)} documents")
    
            # logger.debug(f"sample document:{documents[0]}")
            ids = index.add_documents(documents)
            logger.debug(f"{len(ids)} documents add to index")
            dump(ids, kb_file.id_path)
        # logger.debug(f"{index=}")
        if index.is_local() and do_save:
        # TODO 为何isinstance判断不work？
        # if isinstance(index, LocalVecStore) and do_save:
            logger.info(f"saving {kb_file.file_name} to index dir:{index.local_dir}")
            index.save()

    @log_cost_time(name="rebuild_index")
    def rebuild_index(self, reindex:bool, batch_size:int):
        """
        重新构建向量知识库
        """
        index = self.get_index()
        kb_files = self.list_kb_files()
        for kb_file in kb_files:
            self.add_kb_file2index(index, kb_file, reindex=reindex, do_save=False, batch_size=batch_size)
        if isinstance(index, LocalVecStore):
            index.save()



    @log_cost_time(name="kb_search")
    def search(self, query: str, top_k: int = 3, score_threshold: float = None,
               do_split_query=False, file_names: List[str] = None, rerank_config: dict = {},
               do_expand=False, expand_len: int = 500, forward_rate: float = 0.5) -> List[RecalledChunk]:
        """知识库检索

        Args:
            query (str): 待检索的query
            top_k (int, optional): 返回多少个chunk. Defaults to 3.
            score_threshold (float, optional): 召回的chunk相似度阈值. Defaults to None.
            do_split_query (bool, optional): 是否按照？切分query并分别召回. Defaults to False.
            file_names (List[str], optional): 按照名称过滤需要召回的片段所在的文件. Defaults to None.
            do_expand (bool, optional): 返回的chunk是否做上下文扩展. Defaults to False.
            expand_len (int, optional): 上下文扩展后的chunk字符长度（do_expand=True时生效）. Defaults to 500.
            forward_rate (float, optional): 上下文扩展时向下文扩展的比率（do_expand=True时生效）. Defaults to 0.5.

        Returns:
            List[RecalledChunk]: 相关的切片，按照score降序
        """
        index = self.get_index()
        recalled_chunks = []
        # 切分query
        queries = split_query(query, do_split_query)

        # 将原始score归一化到0-1，越大越接近
        def _get_score(s):
            if self.vecstore_config["distance_strategy"] in [DistanceStrategy.EUCLIDEAN_DISTANCE]:
                return 1.-s
            return s

        # 过滤条件
        _filter = dict()
        if file_names:
            _filter = dict(file_name=file_names)

        # 每个子query做检索
        for query in queries:
            score_threshold = _get_score(score_threshold)
            logger.debug(f"searching {query} with vecstore_cls: {index.__class__.__name__}, {_filter=}, {top_k=}, {score_threshold=}")

            docs_with_score = index.similarity_search_with_score(query, k=top_k, score_threshold=score_threshold, filter=_filter)
            logger.debug(f"{len(docs_with_score)} origin chunks found for {query}")
            # logger.debug(f"{query}'s related docs{[d.page_content[:5] for d,s in docs_with_score]}")
            # logger.debug(docs_with_score[0])

            tmp_recalled_chunks = [RecalledChunk.from_document(d, score=_get_score(s), query=query) for d, s in docs_with_score]
            recalled_chunks.extend(tmp_recalled_chunks)

        # 去重，避免召回相同切片
        recalled_chunks = list(set(recalled_chunks))
        logger.info(f"{len(recalled_chunks)} chunks recalled")

        #重排序
        recalled_chunks = rerank(recalled_chunks, rerank_config)[:top_k]
        logger.info(f"get {len(recalled_chunks)} reranked chunks after sort")

        # 上下文扩展
        if do_expand:
            logger.info("expanding recalled chunks")
            for chunk in recalled_chunks:
                expand_chunk(chunk, expand_len, forward_rate)

        return recalled_chunks


def rerank(recalled_chunks: List[RecalledChunk], rerank_config: dict) -> List[RecalledChunk]:
    """重排序
    Args:
        recalled_chunks (List[RecalledChunk]): 待排序的切片

    Returns:
        List[RecalledChunk]: 排序后的切片
    """
    # logger.debug("reranking...")
    rerank_model = get_rerank_model(rerank_config)
    if rerank_model:
        logger.info("reranking chunks with rerank model")
        for chunk in recalled_chunks:
            similarity = rerank_model.cal_similarity(chunk.query, chunk.content)
            chunk.score = similarity

    recalled_chunks.sort(key=lambda x: x.score, reverse=True)
    return recalled_chunks

def split_query(query: str, do_split_query=False) -> List[str]:
    """切割query"""
    if do_split_query:
        rs = [e.strip() for e in re.split("\?|？", query) if e.strip()]
        logger.debug(f"split origin query into {len(rs)} queries")

        return rs
    else:
        # 不需要切分也转成list形式，方便后续统一处理
        return [query]


# 扩展上下文到给定的长度
#TODO 扩展时，避免重复的chunk
#TODO 扩展时，截断chunk以达到固定数目，Agent问答单测可以检验此问题
def expand_chunk(chunk: RecalledChunk, expand_len: int, forward_rate=0.5) -> RecalledChunk:
    logger.debug(f"expanding chunk {chunk}")
    chunk_path = get_chunk_path(chunk.kb_name, chunk.file_name)
    chunks = []
    for item in load(chunk_path):
        tmp = Chunk(**item)
        chunks.append(tmp)
    chunk_idx = chunk.idx

    to_expand = expand_len - len(chunk.content)
    if to_expand <= 0:
        return chunk

    forward_len = int(to_expand * forward_rate)
    backward_len = to_expand - forward_len
    logger.debug(f"expand chunk with :{forward_len=}, {backward_len=}")
    backwards, forwards = [], []

    # 查找前面的chunk
    idx = chunk_idx-1
    while idx >= 0:
        tmp_chunk = chunks[idx]
        backward_len -= len(tmp_chunk.content)
        if backward_len < 0:
            break
        backwards.append(tmp_chunk)
        idx -= 1
    backwards.reverse()

    idx = chunk_idx + 1
    while idx < len(chunks):
        tmp_chunk = chunks[idx]
        forward_len -= len(tmp_chunk.content)
        if forward_len < 0:
            break
        forwards.append(tmp_chunk)
        idx += 1

    logger.debug(f"expand with {len(backwards)} backward chunks and {len(forwards)} forward chunks")
    chunk.backwards = backwards
    chunk.forwards = forwards
    return chunk
