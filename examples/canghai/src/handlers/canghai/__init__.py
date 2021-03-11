#!/usr/bin/python
# coding=utf8
"""
# Author: wangbin34(meetbill)
# Created Time : 2021-02-23 15:32:03

# File Name: __init__.py
# Description:
    1.0.2 : 2021-03-11
        增加 worker_info 功能

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
__version = "1.0.2"

if "baichuan" in db.my_caches.keys():
    baichuan_connection = db.my_caches["baichuan"]


def _serialize_date(dt):
    """
    将 UTC datetime 转换为 localtime 格式化时间
    """
    if dt is None:
        return "-"

    ds_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    time_stamp = calendar.timegm(time.strptime(ds_str, '%Y-%m-%d %H:%M:%S'))
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))


def _serialize_msg(msg):
    """
    序列化 msg

    Args:
        msg: (object)
    备注:
        msg 为 None 时可能是:
        (1) 从队列、失败、完成 set 中获取到了此 msg ，但此 msg 的 key 已被删除
    """
    if msg is None:
        return dict(
            id="except_msg",
            created_at="-",
            ended_at="-",
            exc_info="get_msg failed",
            description="get_msg_failed"
        )

    return dict(
        id=msg.id,
        created_at=_serialize_date(msg.created_at),
        ended_at=_serialize_date(msg.ended_at),
        exc_info=str(msg.exc_info) if msg.exc_info else None,
        description=msg.description,
    )


def _get_queue_registry_msgs_count(queue_name, registry_name, offset, per_page):
    """
    获取此队列中特定状态的 msg_ids

    Args:
        queue_name: (string)
        registry_name: (string)
        offset: (int) offset_start
        per_page: (int) page_size
    Returns:
        total_items, msg_ids
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
    return (total_items, msg_ids)


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
            created_at=_serialize_date(msg.created_at),
            call_string=msg.get_call_string(),
        )

    workers = sorted(
        (
            dict(
                name=worker.name,
                queues_count=len(worker.queues),
                state=str(worker.get_state()),
                version=getattr(worker, "version", ""),
                python_version=getattr(worker, "python_version", ""),
            )
            for worker in Worker.all(connection=baichuan_connection)
        ),
        key=lambda w: (w["state"], w["queues_count"], w["name"]),
    )
    return retstat.OK, {"data": dict(workers=workers)}, [(__info, __version)]


@funcattr.api
def worker_info(req, name):
    """
    获取 worker 信息
    """
    def serialize_queue_names(worker):
        """
        序列化此 worker 关注的队列名字
        """
        return [q.name for q in worker.queues]

    worker_key = Worker.redis_worker_namespace_prefix + name
    worker = Worker.find_by_key(worker_key, connection=baichuan_connection)
    print worker
    data = dict(
        name=worker.name,
        queues=serialize_queue_names(worker),
        state=str(worker.get_state()),
        version=getattr(worker, "version", ""),
        python_version=getattr(worker, "python_version", ""),
    )

    return retstat.OK, {"data": data}, [(__info, __version)]


@funcattr.api
def list_msgs(req, queue_name, registry_name, page_size=20, page_index=1):
    """
    Args:
        queue_name      : 队列名称
        registry_name   : 任务状态(queued/started/finished/failed)
        page_size       : 每页显示个数
        page_index      : 当前页数
    """

    current_page = int(page_index)
    per_page = int(page_size)

    offset = (current_page - 1) * per_page
    total_items, msg_ids = _get_queue_registry_msgs_count(
        queue_name, registry_name, offset, per_page
    )

    queue = Queue(queue_name, connection=baichuan_connection)
    current_queue_msgs = [queue.fetch_msg(msg_id) for msg_id in msg_ids]
    msgs = [_serialize_msg(msg) for msg in current_queue_msgs]

    data = dict(
        name=queue_name, registry_name=registry_name, msgs=msgs, total_items=total_items
    )
    return retstat.OK, {"data": data}, [(__info, __version)]


@funcattr.api
def msg_info(req, msg_id):
    """
    获取单个消息详情
    Args:
        msg_id: (String) msg id
    """
    msg = Msg.fetch(msg_id, connection=baichuan_connection)
    data = dict(
        id=msg.id,
        msg_data=msg.data,
        created_at=_serialize_date(msg.created_at),
        enqueued_at=_serialize_date(msg.enqueued_at),
        started_at=_serialize_date(msg.started_at),
        ended_at=_serialize_date(msg.ended_at),
        origin=msg.origin,
        status=msg.get_status(),
        result=msg._result,
        exc_info=str(msg.exc_info) if msg.exc_info else None,
        description=msg.description,
    )
    return retstat.OK, {"data": data}, [(__info, __version)]


@funcattr.api
def delete_msg(req, msg_id):
    """
    删除单个消息
    Args:
        msg_id: (String) msg id
    Returns:
        OK
    """
    msg = Msg.fetch(msg_id, connection=baichuan_connection)
    msg.delete()
    return retstat.OK, {}, [(__info, __version)]


@funcattr.api
def empty_queue(req, queue_name, registry_name):
    """
    清空队列

    Args:
        queue_name: (string) queue_name
        registry_name: (string) queued/started/finished/Failed
    Returns:
        OK
    """
    offset = 0
    page_size = 1000

    while True:
        total_items, msg_ids = _get_queue_registry_msgs_count(
            queue_name, registry_name, offset, page_size
        )
        for id in msg_ids:
            delete_msg(req, id)

        if len(msg_ids) < 1000:
            break

        offset = offset + 1
    return retstat.OK, {}, [(__info, __version)]
