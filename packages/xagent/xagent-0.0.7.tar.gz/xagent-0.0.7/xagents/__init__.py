#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/03/01 11:10:10
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


from loguru import logger
from xagents.config import *
from snippets import print_info, set_logger



    
set_logger(env = XAGENT_ENV, module_name=__name__, log_dir=LOG_DIR)
set_logger(XAGENT_ENV, "__main__")


def show_env():
    print_info("current XAgent env", logger)
    logger.info(f"{XAGENT_ENV=}")
    logger.info(f"{KNOWLEDGE_BASE_DIR=}")
    logger.info(f"{TEMP_DIR=}")
    logger.info(f"{LOG_DIR=}")
    logger.info(f"{AGENT_DIR=}")
    logger.info(f"{DATA_DIR=}")
    print_info("", logger)

show_env()


