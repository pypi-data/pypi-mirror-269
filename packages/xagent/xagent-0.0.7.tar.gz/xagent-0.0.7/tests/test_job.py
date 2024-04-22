#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/16 10:43:40
@Author  :   ChenHao
@Description  : job模块的测试脚本
@Contact :   jerrychen1990@gmail.com
'''


from concurrent.futures import ProcessPoolExecutor
 
import time
from unittest import TestCase
from loguru import logger
from snippets import set_logger
from xagents.service.job import Job, JobStatus, get_job_info, init_job_db, stop_job, list_job_infos
from xagents.config import *


def long_time_job(num):
    # print(num)
    logger.info(f"job with {num} seconds started")
    for i in range(num):
        time.sleep(1)
        # print(f"{i+1} seconds passed")
        logger.info(f"{i+1} seconds passed")
    logger.info(f"job with {num} seconds finished")
    return num**2


# unit test
class TestJob(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        init_job_db()
        logger.info("start test job")
        

    def test_list_job_infos(self):
        job_infos = list_job_infos(status=[JobStatus.SUCCESS, JobStatus.FAILED])
        self.assertTrue(len(job_infos)>0, "The list is empty")
        for job_info in job_infos:
            logger.info(f"{job_info=}")        

        
    def test_job(self):
        job_ids =[]
        pool = ProcessPoolExecutor(max_workers=2)
        for t in [5, 10]:
            job:Job = Job.create_job(func=long_time_job, kwargs=dict(num=t)) 
            job_ids.append(job.job_id)
            pool.submit(job.run)
                
        for _ in range(4):
            job_infos = list_job_infos(status=JobStatus.RUNNING)
            for job_info in job_infos:
                logger.info(f"{job_info=}")
            logger.info("waiting 2 seconds...")
            time.sleep(2)
            
        for job_id in job_ids:
            stop_job(job_id=job_id)
            
        # 检测job状态
        EXPECTS = [JobStatus.SUCCESS, JobStatus.STOP]
        for idx, job_id in enumerate(job_ids):
            job_info = get_job_info(job_id)
            logger.info(f"{job_info=}")
            
            self.assertEqual(job_info.status, EXPECTS[idx])
        pool.shutdown()
            
            

