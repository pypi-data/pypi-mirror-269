#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/11 16:40:25
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


from abc import abstractmethod
import enum
from loguru import logger
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from pydantic import BaseModel, Field, ConfigDict, validator
from pandas import DataFrame
from numpy import ndarray
from xagents.config import *



# 切片类型


class ContentType(str, enum.Enum):
    TABLE = "TABLE"
    TITLE = "TITLE"
    TEXT = "TEXT"
    PARSED_TABLE = "PARSED_TABLE"
    IMAGE = "IMAGE"

# 切片

class BBox(BaseModel):
    x0: float
    y0: float
    x1: float
    y1: float
    @property
    def sort_key(self):
        return (self.y0, self.x0)
    
    def to_tuple(self):
        return (self.x0, self.y0, self.x1, self.y1)

class Chunk(BaseModel):
    content: str = Field(description="chunk的内容")
    content_type: ContentType = Field(description="chunk类型", default=ContentType.TEXT)
    search_content: Optional[str] = Field(description="用来检索的内容", default=None)
    page_idx: int = Field(description="chunk在文档中的页码,从1开始")
    
    def to_json(self):
        return self.model_dump(exclude_none=True)


class TextChunk(Chunk):
    content_type:ContentType=ContentType.TEXT
    
class ImageChunk(Chunk):
    content_type:ContentType=ContentType.IMAGE
    content: Optional[str] = Field(description="image的文字描述", default=None)
    url:Optional[str] = Field(description="图片的url", default=None)
    image_name:str = Field(description="图片的文件名")

class TableChunk(Chunk):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    content_type:ContentType=ContentType.TABLE
    data: ndarray|DataFrame = Field(description="表格的数据, 二维数组或pandas的dataframe")
    content: str = Field(description="表格的文字描述, markdown格式", default=None)
    
    def to_json(self):
        return self.model_dump(exclude_none=True, exclude={"data"})


    
    @validator('data', pre=True, always=True)
    def set_content_based_on_data(cls, v, values, **kwargs):
        logger.info(f"{values=}")
        # Check if description is already set
        if values.get("content") is None:
            content = data2markdown(v)
            values["content"] = content
            return v
        return v    


class AbstractLoader:
    def __init__(self, **kwargs) -> None:
        pass
    @abstractmethod
    def load(self, file_path: str,  start_page:int=0, end_page:int=None, store_image=True, ocr=False, **kwargs) -> List[Chunk]:
        raise NotImplementedError


def merge_chunks(chunks: Iterable[Chunk], joiner="\n") -> Iterable[Chunk]:
    acc = None
    cur_page_idx=1
    for chunk in chunks:
        cur_page_idx = chunk.page_idx
        if chunk.content_type == ContentType.TEXT:
            acc = joiner.join([acc, chunk.content]) if acc else chunk.content
        else:
            if acc:
                yield TextChunk(content=acc, page_idx=cur_page_idx)
                acc = None
            yield chunk
    if acc:
        yield TextChunk(content=acc, page_idx=cur_page_idx)
            
        

def upload_image(local_path:str, remote_url:str)->str:
    return f"{remote_url}/{local_path}"


def get_image_name_path(kf_file_name:str, page_idx:int, image_idx:int)->Tuple[str, str]:
    image_name =f"{Path(kf_file_name).stem}-page{page_idx}-image{image_idx}.png"
    file_path = os.path.join(TEMP_DIR, "extracted_images", image_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return image_name, file_path

def data2markdown(data:ndarray|DataFrame)->str:
    if isinstance(data, ndarray):
        data = DataFrame(data)
    data.fillna("", inplace=True)
    markdown = data.to_markdown(index=False)
    return markdown
