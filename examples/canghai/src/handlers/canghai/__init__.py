#!/usr/bin/python
# coding=utf8
"""
# Author: wangbin34(meetbill)
# Created Time : 2021-02-23 15:32:03

# File Name: __init__.py
# Description:

"""
import time
import calendar

from xlib import retstat
from xlib import db
from xlib.middleware import funcattr
from xlib.mq.msg import Msg
from xlib.mq import Worker
from xlib.mq import Queue
from xlib.mq.registry import (
    FailedMsgRegistry,
    FinishedMsgRegistry,
    StartedMsgRegistry,
)

__info = "canghai"
__version = "1.0.1"

if "baichuan" in db.my_caches.keys():
    baichuan_connection = db.my_caches["baichuan"]

def serialize_date(dt):
    """
    将 UTC datetime 转换为 localtime 格式化时间
    """
    ds_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    time_stamp = calendar.timegm(time.strptime(ds_str, '%Y-%m-%d %H:%M:%S'))
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))


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
                        'failed_msg_registry_count': 6,
                        'name': u'default',
                        'deferred_msg_registry_count': 0,
                        'finished_msg_registry_count': 0,
                        'started_msg_registry_count': 0
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
                failed_msg_registry_count=FailedMsgRegistry(q.name, connection=baichuan_connection).count,
                started_msg_registry_count=StartedMsgRegistry(q.name, connection=baichuan_connection).count,
                finished_msg_registry_count=FinishedMsgRegistry(q.name, connection=baichuan_connection).count,
            )
            for q in queues
        ]

    queues = serialize_queues(sorted(Queue.all(connection=baichuan_connection)))
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
    def serialize_current_msg(msg):
        """
        序列化当前的任务
        """
        if msg is None:
            return "idle"
        return dict(
            msg_id=msg.id,
            description=msg.description,
            created_at=serialize_date(msg.created_at),
            call_string=msg.get_call_string(),
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
                version=getattr(worker, "version", ""),
                python_version=getattr(worker, "python_version", ""),
            )
            for worker in Worker.all(connection=baichuan_connection)
        ),
        key=lambda w: (w["state"], w["queues"], w["name"]),
    )
    return retstat.OK, {"data": dict(workers=workers)}, [(__info, __version)]


@funcattr.api
def list_msgs(req, queue_name, registry_name, page_size=20, page_index=1):
    """
    Args:
        queue_name      : 队列名称
        registry_name   : 任务状态(queued/started/finished/failed)
        page_size       : 每页显示个数
        page_index      : 当前页数
    """
    def serialize_msg(msg):
        """
        序列化 msg
        """
        return dict(
            id=msg.id,
            created_at=serialize_date(msg.created_at),
            ended_at=serialize_date(msg.ended_at),
            exc_info=str(msg.exc_info) if msg.exc_info else None,
            description=msg.description,
        )

    def get_queue_registry_msgs_count(queue_name, registry_name, offset, per_page):
        """
        获取此队列中特定状态的 msgs
        """
        queue = Queue(queue_name, connection=baichuan_connection)
        if registry_name != "queued":
            if per_page >= 0:
                per_page = offset + (per_page - 1)

            if registry_name == "failed":
                current_queue = FailedMsgRegistry(queue_name, connection=baichuan_connection)
            elif registry_name == "started":
                current_queue = StartedMsgRegistry(queue_name, connection=baichuan_connection)
            elif registry_name == "finished":
                current_queue = FinishedMsgRegistry(queue_name, connection=baichuan_connection)
        else:
            current_queue = queue

        # 队列中此状态 msg 的总数
        total_items = current_queue.count

        msg_ids = current_queue.get_msg_ids(offset, per_page)
        current_queue_msgs = [queue.fetch_msg(msg_id) for msg_id in msg_ids]
        msgs = [serialize_msg(msg) for msg in current_queue_msgs]

        return (total_items, msgs)

    current_page = int(page_index)
    per_page = int(page_size)

    offset = (current_page - 1) * per_page
    total_items, msgs = get_queue_registry_msgs_count(
        queue_name, registry_name, offset, per_page
    )


    data = dict(
        name=queue_name, registry_name=registry_name, msgs=msgs, total_items=total_items
    )
    return retstat.OK, {"data": data}, [(__info, __version)]


@funcattr.api
def msg_info(req, msg_id):
    msg = Msg.fetch(msg_id, connection=baichuan_connection)
    data = dict(
        id=msg.id,
        created_at=serialize_date(msg.created_at),
        enqueued_at=serialize_date(msg.enqueued_at),
        ended_at=serialize_date(msg.ended_at),
        origin=msg.origin,
        status=msg.get_status(),
        result=msg._result,
        exc_info=str(msg.exc_info) if msg.exc_info else None,
        description=msg.description,
    )
    return retstat.OK, {"data": data}, [(__info, __version)]
