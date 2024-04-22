#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/12 11:34:29
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

from typing import List
from fastapi import UploadFile
from loguru import logger
from pydantic import BaseModel, Field
from xagents.kb.kb_file import KnowledgeBaseFile
from xagents.kb.kb import KnowledgeBase
from xagents.config import *
from xagents.kb.common import KnowledgeBaseInfo, KnowledgeBaseFileInfo, RecalledChunk, get_config_path, get_kb_dir, DistanceStrategy


def list_knowledge_base_names() -> List[str]:
    """列出所有知识库名称

    Returns:
        str: 知识库名称列表
    """
    kb_names = os.listdir(KNOWLEDGE_BASE_DIR)
    return kb_names

def list_knowledge_base_info() -> List[KnowledgeBaseInfo]:
    kb_infos = []
    kb_names=  list_knowledge_base_names()
    for name in kb_names:
        kb = get_knowledge_base(name)
        kb_infos.append(kb.get_info())
    return kb_infos
    

def get_knowledge_base(name: str) -> KnowledgeBase:
    """根据知识库名称获取知识库

    Args:
        name (str): 知识库名称

    Raises:
        ValueError: 知识库不存在异常

    Returns:
        KnowledgeBase: 知识库实例
    """
    config_path = get_config_path(name)
    if not os.path.exists(config_path):
        message = f"知识库配置文件不存在: {config_path}"
        logger.error(message)
        raise ValueError(message)
    kb = KnowledgeBase.from_config(config_path)
    return kb


def get_knowledge_base_info(name: str) -> KnowledgeBaseInfo:
    """
    根据名称获取知识库实例
    """
    kb = get_knowledge_base(name=name)
    return kb.get_info()


def create_knowledge_base(name: str,
                          desc: str = None,
                          embedding_config: dict = dict(cls="ZhipuEmbedding"),
                          vecstore_config: dict = dict(cls='XFAISS', distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT)
                          ) -> KnowledgeBaseInfo:
    """创建知识库

    Raises:
        ValueError: 知识库已经存在的异常

    Returns:
        _type_: _description_
    """

    logger.info(f"Creating knowledge base {name}...")
    kb_names = list_knowledge_base_names()
    if name in kb_names:
        msg = f"Knowledge base {name} already exists, can not create!"
        logger.warning(msg)
        raise ValueError(msg)
    if not desc:
        desc = f"知识库{name}"
    kb = KnowledgeBase(name=name, embedding_config=embedding_config,
                       desc=desc, vecstore_config=vecstore_config)
    return kb.get_info()


def delete_knowledge_base(name: str) -> str:
    """删除知识库

    Args:
        name (str): 知识库名称

    Returns:
        str: 删除消息
    """
    # delete knowledge base
    kb_dir = get_kb_dir(kb_name=name)
    if os.path.exists(kb_dir):
        import shutil
        shutil.rmtree(path=kb_dir)
    msg = f'【{name}】deleted.'
    return msg


def reindex_knowledge_base(name: str, reindex=True, batch_size=16) -> str:
    """重新构建知识库索引

    Args:
        name (str): 知识库名称
        reindex(bool): 对于已经索引好的文件是否重新embedding
        batch_size(int): 调用embedding的时候的batch_size（对于开发平台api,是并发度）
    """
    kb = get_knowledge_base(name=name)
    kb.rebuild_index(reindex=reindex, batch_size=batch_size)
    msg = f"知识库【{name}】重建索引成功"
    return msg


class KBSearchConfig(BaseModel):
    top_k:int = Field(default=3, description="返回几个chunk")
    score_threshold:float = Field(default=0., description="分数阈值")
    do_split_query:bool = Field(default=False, description="是否分词")
    file_names:List[str] = Field(default=[], description="需要筛选的知识库文件文件名列表")
    rerank_config:dict = Field(default={}, description="rerank的配置")
    do_expand:bool = Field(default=False, description="对结果是否进行上下文扩展")
    expand_len:int = Field(default=500, description="上下文扩展的长度")
    forward_rate:float = Field(default=0.5, description="上下文扩展向下扩展的比例")
    

def search_knowledge_base(name: str,
                          query: str, top_k: int = 3, score_threshold: float = None,
                          do_split_query=False, file_names: List[str] = [], rerank_config: dict = {},
                          do_expand=False, expand_len: int = 500, forward_rate: float = 0.5) -> List[RecalledChunk]:
    kb = get_knowledge_base(name=name)
    
    chunks = kb.search(query=query, top_k=top_k, score_threshold=score_threshold, do_split_query=do_split_query,
                       file_names=file_names, rerank_config=rerank_config, do_expand=do_expand, expand_len=expand_len, forward_rate=forward_rate)
    return chunks


def list_kb_file_infos(kb_name: str) -> List[KnowledgeBaseFileInfo]:
    kb = get_knowledge_base(kb_name)
    kb_files = kb.list_kb_files()
    kb_file_infos = [kb_file.get_info() for kb_file in kb_files]
    return kb_file_infos


def get_kb_file(kb_name: str, file_name: str) -> KnowledgeBaseFile:
    kb_file = KnowledgeBaseFile(kb_name=kb_name, file_name=file_name)
    if os.path.exists(kb_file.origin_path):
        return kb_file
    raise ValueError(f"{kb_file.origin_path} not exists.")


def get_kb_file_info(kb_name: str, file_name: str) -> KnowledgeBaseFileInfo:
    kb_file = get_kb_file(kb_name=kb_name, file_name=file_name)
    return kb_file.get_info()


def create_kb_file(kb_name: str, file: UploadFile | str, do_cut=True, do_index=True,
                   batch_size:int=16,
                   cut_config: dict = dict(separator='\n',
                                           max_len=200,
                                           min_len=10)) -> KnowledgeBaseFileInfo:
    """创建知识库文件
    Args:
        kb_name (str): 知识库名称
        file (UploadFile | str): 知识库文件，UploadFile(fast_api)或者str(文件路径)
        do_cut (bool, optional): 是否切分文件. Defaults to True.
        do_index (bool, optional): 是否添加到索引. Defaults to True.
        cut_config (dict, optional): 切分文件的参数. Defaults to dict(separator='\n', max_len=200, min_len=10).

    Raises:
        ValueError: 知识库文件已经存在

    Returns:
        KnowledgeBaseFileInfo: 知识库文件描述
    """
    if isinstance(file, str):
        file_name = os.path.basename(file)
    else:
        file_name = os.path.basename(file.filename)
    logger.debug(f"creating kb_file with {kb_name=}, {file_name=}")
    kb_file = KnowledgeBaseFile(kb_name=kb_name, file_name=file_name)
    kb_file_path = kb_file.origin_path
    if os.path.exists(kb_file_path):
        raise ValueError(f"{kb_file_path} already exists.")
    if isinstance(file, str):
        with open(file, "rb") as f:
            content = f.read()
    else:
        content = file.file.read()
    with open(kb_file_path, "wb") as f:
        f.write(content)
    if do_cut:
        kb_file.cut(**cut_config)
    if do_index:
        kb = get_knowledge_base(name=kb_name)
        index = kb.get_index()
        # logger.debug(f"{index=}")
        kb.add_kb_file2index(index, kb_file, reindex=True, do_save=True,batch_size=batch_size)
    kb_file_info = kb_file.get_info()
    return kb_file_info


def delete_kb_file(kb_name: str, file_name: str) -> str:
    """删除知识库文件

    Args:
        kb_name (str): 知识库名称
        file_name (str): 知识库文件名称

    Returns:
        str: 删除消息
    """

    kb = get_knowledge_base(kb_name)
    kb_file = get_kb_file(kb_name=kb_name, file_name=file_name)
    kb.remove_file(kb_file=kb_file)
    return f"知识库文件【{file_name}】删除成功"


def cut_kb_file(kb_name: str, file_name: str,
                separator: str = '\n',
                max_len: int = 200,
                min_len: int = 10) -> int:
    """切分文档，并且按照jsonl格式存储在chunk目录下

    Args:
        kb_name (str): 知识库名称
        file_name (str): 文件名称
        separator (str, optional): 切分符. Defaults to '\n'.
        max_len (int, optional): 最大切片长度. Defaults to 200.
        min_len (int, optional): 最小切片长度. Defaults to 10.

    Returns:
        int: 切片数目
    """

    kb_file = get_kb_file(kb_name=kb_name, file_name=file_name)
    chunk_num = kb_file.cut(separator=separator, max_len=max_len, min_len=min_len)
    return chunk_num


def reindex_kb_file(kb_name: str, file_name: str, reindex=False,  batch_size=16) -> str:
    """添加知识库文件到索引中

    Args:
        kb_name (str): 知识库名称
        file_name (str): 知识库文件名称
        reindex (bool, optional): 如果知识库文件已经存在，是否重新构建索引. Defaults to False.

    Returns:
        str: 构建成功的消息
    """

    kb = get_knowledge_base(kb_name)
    kb_file = get_kb_file(kb_name=kb_name, file_name=file_name)
    kb.add_kb_file2index(index=kb.get_index(), kb_file=kb_file, reindex=reindex, do_save=True, batch_size=batch_size)
    return f"更新知识库文件【{file_name}】到索引成功"


if __name__ == "__main__":
    # print(list_knowledge_base_names())
    # print(list_vecstores())
    # print(list_distance_strategy())
    # chunk_len = cut_kb_file(kb_name="new_kb", file_name="requirements.txt")
    # print(chunk_len)

    kb = get_knowledge_base(name="new_kb")
    chunks = kb.search(query="python-snippets", score_threshold=0.4)
    print(chunks)
