#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/03/19 16:24:43
@Author  :   ChenHao
@Description  : 文档处理对外接口
@Contact :   jerrychen1990@gmail.com
'''

import os
from loguru import logger
from typing import Iterable, List, Type
from xagents.loader.pdf_loader import PDFLoader
from xagents.loader.docx_loader import DOCXLoader

from xagents.loader.markdown import MarkDownLoader
from xagents.loader.structed import StructedLoader
from xagents.loader.common import Chunk, AbstractLoader

from xagents.loader.splitter import BaseSplitter
from snippets import flat, log_cost_time

_EXT2LOADER = {
    "pdf": PDFLoader,
    "markdown": MarkDownLoader,
    "md": MarkDownLoader,
    "json": StructedLoader,
    "jsonl": StructedLoader,
    "csv": StructedLoader,
    "txt": MarkDownLoader,
    "docx": DOCXLoader,
    "": MarkDownLoader
}


def get_loader_cls(file_path: str) -> Type[AbstractLoader]:
    """根据file路径后缀，加载对应的文档加载器

    Args:
        file_path (str): 文件后缀

    Raises:
        ValueError: 非法后缀异常

    Returns:
        Type[AbstractLoader]: 文档加载器class
    """
    ext = os.path.splitext(file_path)[-1].lower().replace(".", "")
    if ext not in _EXT2LOADER:
        msg = f"{ext} not support!"
        raise ValueError(msg)

    loader_cls = _EXT2LOADER[ext]
    return loader_cls


@log_cost_time(name="load file", logger=logger)
def load_file(file_path: str, start_page: int = 1, end_page: int = None, upload_image=True, ocr=False, **kwargs) -> Iterable[Chunk]:
    """处理文档，返回文档切片

    Args:
        file_path (str): 文档路径
        start_page (int, optional): 开始页码. Defaults to 1.
        end_page (int, optional): 结束页码,None表示到最后一页结束. Defaults to None.
        upload_image (bool, optional): 是否存储图片并上传到图片服务器. Defaults to True.
        ocr (bool, optional): 是否使用ocr识别图片中的文字. Defaults to False.

    Returns:
        Iterable[Chunk]: 切片列表
    """
    loader_cls = get_loader_cls(file_path)
    loader: AbstractLoader = loader_cls(**kwargs)
    logger.debug(f"loading {file_path} with loader:{loader}")
    pages = loader.load(file_path, start_page=start_page, end_page=end_page, upload_image=upload_image, ocr=ocr,
                        **kwargs)
    return pages


def convert2txt(file_path: str, dst_path: str = None, **kwargs) -> str:
    """将原始文件转移成txt格式

    Args:
        file_path (str): 原始文件路径
        dst_path (str, optional): 目标路径，未传的话，和原始文件同目录. Defaults to None.

    Returns:
        str: 目标路径
    """
    chunks = load_file(file_path, **kwargs)
    if not dst_path:
        dst_path = file_path+".txt"
    with open(dst_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(chunk.content)
    return dst_path


def parse_file(file_path: str,
               start_page: int = 1, 
               end_page: int = None, 
               upload_image=True,
                ocr=False,
               do_cut: bool = True,
               separator: str = '\n',
               max_len: int = 200,
               min_len: int = 10) -> List[Chunk]:
    """加载并切分切片

    Args:
        file_path (str): 文件路径
        start_page (int, optional): 开始页码. Defaults to 1.
        end_page (int, optional): 结束页码. Defaults to None.
        upload_image (bool, optional): 是否上传图片到存储服务器. Defaults to True.
        ocr (bool, optional): 是否调用ocr. Defaults to False.
        do_cut (bool, optional): 是否切片. Defaults to True.
        separator (str, optional): 分隔符. Defaults to '\n'.
        max_len (int, optional): 最大切片长度. Defaults to 200.
        min_len (int, optional): 最小切片长度. Defaults to 10.

    Returns:
        List[Chunk]: 切片列表
    """

    splitter = BaseSplitter(max_len=max_len, min_len=min_len, separator=separator)
    origin_chunks: Iterable[Chunk] = load_file(file_path=file_path, start_page=start_page,
                                               end_page=end_page, upload_image=upload_image, ocr=ocr)
    origin_chunks = list(origin_chunks)
    logger.debug(f"load {len(origin_chunks)} origin_chunks")
    if do_cut:
        split_chunks = flat([splitter.split_chunk(origin_chunk) for origin_chunk in origin_chunks])
        logger.info(f"split {len(origin_chunks)} origin_chunks to {len(split_chunks)} chunks")
        return split_chunks
    else:
        return origin_chunks


if __name__ == "__main__":
    file_path = "/Users/chenhao/Downloads/汽车手册V16.txt"

    chunks = parse_file(file_path, do_cut=True, separator="==")
    print(f"{len(chunks)=}")
    for chunk in chunks[:4]:
        print(chunk)
        # print(chunk.content)
