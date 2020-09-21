#!/usr/bin/python
# coding=utf8
"""
# Author: wangbin34(meetbill)
# Created Time : 2020-02-23 21:40:27

# File Name: __init__.py
# Description:
    沧海 API

"""
from xlib.middleware import funcattr

__info = "canghai"
__version = "1.0.1"

from xlib.db import redis
from xlib import retstat


from xlib.mq.rq.job import Job
from xlib.mq.rq import Worker
from xlib.mq.rq import Queue
from xlib.mq.rq.registry import (
    DeferredJobRegistry,
    FailedJobRegistry,
    FinishedJobRegistry,
    StartedJobRegistry,
)


pool = redis.ConnectionPool(db=0, host='localhost', port=6379)
redis_conn = redis.Redis(connection_pool=pool)


@funcattr.api
def list_queues(req):
    """
    queue 列表

    返回：
        'OK',
        {
            'data':{
                'queues': [
                    {
                        'count': 0,
                        'failed_job_registry_count': 6,
                        'name': u'default',
                        'deferred_job_registry_count': 0,
                        'finished_job_registry_count': 0,
                        'started_job_registry_count': 0
                    }
                ]
            }
        },
        [('canghai', '1.0.1')]

    """
    def serialize_queues(queues):
        """
        Args:
            queues: List, 如 [Queue(u'default')]
        """
        return [
            dict(
                name=q.name,
                count=q.count,
                failed_job_registry_count=FailedJobRegistry(q.name, connection=redis_conn).count,
                started_job_registry_count=StartedJobRegistry(q.name, connection=redis_conn).count,
                deferred_job_registry_count=DeferredJobRegistry(q.name, connection=redis_conn).count,
                finished_job_registry_count=FinishedJobRegistry(q.name, connection=redis_conn).count,
            )
            for q in queues
        ]

    queues = serialize_queues(sorted(Queue.all(connection=redis_conn)))
    return retstat.OK, {"data": dict(queues=queues)}, [(__info, __version)]


@funcattr.api
def list_workers(req):
    """
    worker 列表

    返回:
        'OK',
        {
            'data': {
                'workers': [
                    {
                        'current_job': 'idle',
                        'state': 'idle',
                        'version': u'1.3.0',
                        'python_version': u'2.7.3 ()]',
                        'queues': [u'high', u'default', u'low'],
                        'name': u'108585d59bfe40959b49b372a304a6fe'
                    }
                ]
            }
        },
        [('canghai', '1.0.1')]
    """
    def serialize_current_job(job):
        """
        序列化当前的任务
        """
        if job is None:
            return "idle"
        return dict(
            job_id=job.id,
            description=job.description,
            created_at=job.created_at,
            call_string=job.get_call_string(),
        )

    def serialize_queue_names(worker):
        """
        序列化此 worker 关注的队列名字
        """
        return [q.name for q in worker.queues]

    workers = sorted(
        (
            dict(
                name=worker.name,
                queues=serialize_queue_names(worker),
                state=str(worker.get_state()),
                current_job=serialize_current_job(worker.get_current_job()),
                version=getattr(worker, "version", ""),
                python_version=getattr(worker, "python_version", ""),
            )
            for worker in Worker.all(connection=redis_conn)
        ),
        key=lambda w: (w["state"], w["queues"], w["name"]),
    )
    return retstat.OK, {"data": dict(workers=workers)}, [(__info, __version)]


@funcattr.api
def list_jobs(req, queue_name, registry_name, page_size=20, page_index=1):
    """
    Args:
        queue_name      : 队列名称
        registry_name   : 任务状态(queued/deferred/started/finished/failed)
        page_size       : 每页显示个数
        page_index      : 当前页数
    """
    def serialize_job(job):
        """
        序列化 job
        """
        return dict(
            id=job.id,
            created_at=job.created_at,
            ended_at=job.ended_at,
            exc_info=str(job.exc_info) if job.exc_info else None,
            description=job.description,
        )

    def get_queue_registry_jobs_count(queue_name, registry_name, offset, per_page):
        """
        获取此队列中特定状态的 jobs
        """
        queue = Queue(queue_name, connection=redis_conn)
        if registry_name != "queued":
            if per_page >= 0:
                per_page = offset + (per_page - 1)

            if registry_name == "failed":
                current_queue = FailedJobRegistry(queue_name, connection=redis_conn)
            elif registry_name == "deferred":
                current_queue = DeferredJobRegistry(queue_name, connection=redis_conn)
            elif registry_name == "started":
                current_queue = StartedJobRegistry(queue_name, connection=redis_conn)
            elif registry_name == "finished":
                current_queue = FinishedJobRegistry(queue_name, connection=redis_conn)
        else:
            current_queue = queue

        # 队列中此状态 job 的总数
        total_items = current_queue.count

        job_ids = current_queue.get_job_ids(offset, per_page)
        current_queue_jobs = [queue.fetch_job(job_id) for job_id in job_ids]
        jobs = [serialize_job(job) for job in current_queue_jobs]

        return (total_items, jobs)

    current_page = int(page_index)
    per_page = int(page_size)

    offset = (current_page - 1) * per_page
    total_items, jobs = get_queue_registry_jobs_count(
        queue_name, registry_name, offset, per_page
    )

    data = dict(
        name=queue_name, registry_name=registry_name, jobs=jobs, total_items=total_items
    )
    return retstat.OK, {"data": data}, [(__info, __version)]


@funcattr.api
def job_info(req, job_id):
    job = Job.fetch(job_id, connection=redis_conn)
    data = dict(
        id=job.id,
        created_at=job.created_at,
        enqueued_at=job.enqueued_at,
        ended_at=job.ended_at,
        origin=job.origin,
        status=job.get_status(),
        result=job._result,
        exc_info=str(job.exc_info) if job.exc_info else None,
        description=job.description,
    )
    return retstat.OK, {"data": data}, [(__info, __version)]
