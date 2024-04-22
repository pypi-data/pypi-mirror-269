#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/11 16:42:25
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

import numpy as np
from loguru import logger
from typing import Iterable, List, Tuple


from xagents.config import *
from xagents.loader.common import BBox, Chunk, TableChunk, TextChunk, ImageChunk, get_image_name_path, merge_chunks, upload_image as do_upload_image, AbstractLoader
from pdfplumber.page import Page




def analyse_page(idx:int, page:Page, file_name:str, upload_image:bool, ocr:bool)->Iterable[Chunk]:
            
    chunks:List[Tuple[Chunk, BBox]] = []  # List to store all content with their position

    # 抽取文本
    for line in  page.extract_text_lines(x_tolerance=3, y_tolerance=3):
        chunks.append((TextChunk(content=line['text'], page_idx=idx), BBox(x0=line["x0"], y0=line["top"], x1=line["x1"], y1=line["bottom"])))

    # Extract tables and add to content list
    # tables = page.extract_tables({
    #     "horizontal_strategy": "text",
    #     "vertical_strategy": "text",
    # })
    # print(tables)
    tables = page.extract_tables()
    for table in tables:
        bbox = BBox(x0=0, x1=0, y0=0, y1=0)
        # logger.info(f"table: {table}")

        table = np.array(table)
        chunks.append((TableChunk(data=table, page_idx=idx), bbox))

    # Extract images and add to content list
    page_image = page.to_image().original
    for i, image in enumerate(page.images):
        bbox = BBox(x0=image['x0'], y0=image['top'], x1=image['x1'], y1=image['bottom'])
        # pil_image = Image.open(page_image.annotated)
        image = page_image.crop(bbox.to_tuple())
        
        
        image_name, image_path =get_image_name_path(file_name, idx, i)     
        if upload_image:
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path, format="PNG")
            url= do_upload_image(image_path, "http://cdn/")
        else:
            url=None
        if ocr:
            #TODO 调用ocr
            content = ""
        else:
            content = None
        chunks.append((ImageChunk(url=url, content=content, image_name=image_name, page_idx=idx), bbox))
        
    chunks.sort(key=lambda x: x[1].sort_key)  # Sort by top y coordinate, then by left x coordinate
    yield from (x[0] for x in chunks)



class PDFLoader(AbstractLoader):
    def load(self, file_path: str, start_page=1, end_page=None, upload_image=True, ocr=False) -> Iterable[Chunk]:
        import pdfplumber

        logger.info(f"loading pdf file {file_path} from {start_page} to {end_page}, {upload_image=}, {ocr=}")
        pages = pdfplumber.open(file_path)
        for idx, page in enumerate(pages.pages, start=1):
            if idx < start_page:
                continue
            if end_page and idx > end_page:
                break
            chunks = analyse_page(idx, page, os.path.basename(file_path), upload_image=upload_image, ocr=ocr)
            yield from merge_chunks(chunks=chunks)

            


if __name__ == "__main__":
    from xagents.config import XAGENT_HOME
    import sys
    import pdfplumber
    logger.add(sys.stdout)
    doc_path = os.path.join(XAGENT_HOME, "data/kb_file/image_table.pdf")
    pages = pdfplumber.open(doc_path)
    pages = list(pages.pages)
    contents = analyse_page(pages[4])
    for content in contents:
        
        print(content)    

