#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/08 16:57:23
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

import copy
import os
from typing import List, Type
from langchain.vectorstores.faiss import FAISS
import faiss
from langchain.vectorstores import VectorStore
from langchain.docstore.in_memory import InMemoryDocstore
from langchain.vectorstores.elasticsearch import ElasticsearchStore
from langchain.vectorstores import VectorStore as VectorStore

from xagents.model.common import EMBD
from xagents.kb.common import DistanceStrategy

from loguru import logger


class XVecStore(VectorStore):
    @classmethod
    def is_local(cls) -> bool:
        raise NotImplementedError()

    @classmethod
    def need_embd(cls):
        raise NotImplementedError()

    @classmethod
    def from_config(cls, config: dict):
        raise NotImplementedError()


class LocalVecStore(VectorStore):
    def __init__(self, local_dir: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.local_dir = local_dir

    @classmethod
    def is_local(cls):
        return True

    @classmethod
    def load_local(cls):
        pass

    def save(self, *args, **kwargs):
        pass


class XFAISS(LocalVecStore, FAISS):
    @classmethod
    def is_local(cls):
        return True

    @classmethod
    def need_embd(cls):
        return False

    @classmethod
    def from_config(cls, config: dict) ->"XFAISS":
        local_dir: str = config["local_dir"]
        embedding: EMBD = config["embedding"]
        distance_strategy = config.get("distance_strategy", DistanceStrategy.MAX_INNER_PRODUCT)

        if os.path.exists(local_dir):
            logger.info(f"loading vecstore from {local_dir}")
            vecstore = cls.load_local(local_dir=local_dir, embedding=embedding, distance_strategy=distance_strategy)
        else:
            logger.info(f"{local_dir} not exists, create a new local vecstore")

            dim_len = embedding.get_dim()

            # faiss = dependable_faiss_import()
            if distance_strategy == DistanceStrategy.MAX_INNER_PRODUCT:
                index = faiss.IndexFlatIP(dim_len)
            else:
                # Default to L2, currently other metric types not initialized.
                index = faiss.IndexFlatL2(dim_len)
            vecstore = cls(
                local_dir=local_dir,
                index=index, embedding_function=embedding,  index_to_docstore_id=dict(),
                docstore=InMemoryDocstore(), distance_strategy=distance_strategy
            )
        return vecstore

    @classmethod
    def load_local(cls, local_dir:str, embedding:EMBD, distance_strategy:DistanceStrategy,  **kwargs) -> "XFAISS":
        faiss = FAISS.load_local(folder_path=local_dir, allow_dangerous_deserialization=True, embeddings=embedding)
        return XFAISS(local_dir=local_dir, embedding_function=embedding, distance_strategy=distance_strategy,
                       index=faiss.index, docstore=faiss.docstore, index_to_docstore_id=faiss.index_to_docstore_id)

    def save(self, *args, **kwargs):
        return self.save_local(folder_path=self.local_dir, *args, **kwargs)

    def delete(self, ids: List[str], *args, **kwargs) -> int:
        ids = list(set(ids) & set(self.index_to_docstore_id.values()))
        if not ids:
            logger.warning("no overlap id, will not delete from index")
        else:
            logger.debug(f"deleting {len(ids)} vec from index")
            super().delete(ids, *args, **kwargs)
        return len(ids)


class XES(XVecStore, ElasticsearchStore):
    @classmethod
    def is_local(cls):
        return False

    @classmethod
    def need_embd(cls):
        return True

    @classmethod
    def from_config(cls, config: dict):
        vecstore = cls(
            **config
        )
        return vecstore


_vecstores = [XFAISS, XES]
_name2vecstores = {e.__name__: e for e in _vecstores}


def list_vecstores():
    return [e.__name__ for e in _vecstores]


def get_vecstore_cls(name: str) -> Type[XVecStore]:
    return _name2vecstores[name]


def get_vector_store(config: dict, embd_model: EMBD = None) -> XVecStore:
    tmp_config = copy.copy(config)
    vs_cls = tmp_config.pop("vs_cls")
    vs_cls = get_vecstore_cls(vs_cls)
    logger.debug(f"getting vecstore with config:{config}")
    # if vs_cls.need_embd():
    #     if embd_model is None:
    #         raise ValueError("Need embd model to create vector store")
    tmp_config.update(embedding=embd_model)
    return vs_cls.from_documents([], **tmp_config)
