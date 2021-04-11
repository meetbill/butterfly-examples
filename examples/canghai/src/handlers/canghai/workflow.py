#!/usr/bin/python
# coding=utf8
"""
# Author: wangbin34
# Created Time : 2021-04-11 15:10:56

# File Name: workflow.py
# Description:
    1.0.1 : 2021-04-11

"""
import os

from conf import config
from xlib import retstat
from xlib.middleware import funcattr
from xlib.httpgateway import Request
from xlib.pyflow import model
from xlib.pyflow import gen_graph
from xlib.db import peewee
from xlib.db import shortcuts
from xlib.util import shell_util


__info = "canghai_workflow"
__version = "1.0.5"


@funcattr.api
def list_jobs(req, job_reqid=None, job_id=None, job_name=None, job_runner=None,
              job_status=None, job_type=None, job_retcode=None, page_index=1, page_size=10):
    """
    Args:
        state       : (str) job 状态
        page_index  : (int) 页数
        page_size   : (int) 每页显示条数

    Returns:
        {
            'data': {
                'total': 1,
                'list': [
                    {
                        'job_runner': u'xxxxx:8033:31827',
                        'job_status': u'failed',
                        'job_reqid': u'329FE02D1CF75155',
                        'job_id': 3,
                        'job_retinfo': u'',
                        'c_time': datetime.datetime(2021, 4, 11, 16, 27, 26),
                        'u_time': datetime.datetime(2021, 4, 11, 16, 27, 27),
                        'job_cost': 1.06245994567871,
                        'job_type': u'HelloWorkflow',
                        'job_retcode': 1,
                        'job_name': u'ceshi',
                        'job_extra': u'{}'
                    }
                ]
            }
        }

    """
    isinstance(req, Request)
    data = {}
    data_list = []

    # 如下方式以分页数据返回
    query_cmd = model.Job.select()
    expressions = []
    if job_reqid is not None:
        expressions.append(peewee.NodeList((model.Job.job_reqid, peewee.SQL('='), job_reqid)))

    if job_runner is not None:
        expressions.append(peewee.NodeList((model.Job.job_id, peewee.SQL('LIKE'), job_runner)))

    if job_id is not None:
        expressions.append(peewee.NodeList((model.Job.job_id, peewee.SQL('='), int(job_id))))

    if job_name is not None:
        expressions.append(peewee.NodeList((model.Job.job_name, peewee.SQL('LIKE'), job_name)))

    if job_status is not None:
        expressions.append(peewee.NodeList((model.Job.job_status, peewee.SQL('='), job_status)))

    if job_type is not None:
        expressions.append(peewee.NodeList((model.Job.job_type, peewee.SQL('='), job_type)))

    if job_retcode is not None:
        expressions.append(peewee.NodeList((model.Job.job_retcode, peewee.SQL('='), job_retcode)))

    if len(expressions):
        query_cmd = query_cmd.where(*expressions)

    record_count = query_cmd.count()
    record_list = query_cmd.order_by(model.Job.c_time.desc()).paginate(int(page_index), int(page_size))

    for record in record_list:
        record_dict = shortcuts.model_to_dict(record)
        data_list.append(record_dict)

    data["total"] = record_count
    data["list"] = data_list
    return retstat.OK, {"data": data}, [(__info, __version)]


@funcattr.api
def get_job_detail(req, job_id):
    """
    Returns:
        {
            'data': {
                'job_runner': u'xxxxx:8033:6140',
                'job_status': u'failed',
                'job_reqid': u'DEV_DD99CB8BFEE09FAC',
                'job_id': 1,
                'job_retinfo': u'',
                'c_time': datetime.datetime(2021, 4, 11, 17, 31, 59),
                'u_time': datetime.datetime(2021, 4, 11, 17, 32, 4),
                'job_cost': 5.63627195358276,
                'job_type': u'HelloWorkflow',
                'job_retcode': 1,
                'job_name': u'ceshi',
                'job_extra': u'{}'
            }
        }
    """
    isinstance(req, Request)
    job = model.Job.get_or_none(job_id=int(job_id))
    if job is None:
        return "ERR_JOB_NOT_EXIST", {"data": {}}, [(__info, __version)]

    job_dict = shortcuts.model_to_dict(job)
    return retstat.OK, {"data": job_dict}, [(__info, __version)]


@funcattr.api
def get_tasklist_by_jobid(req, job_id):
    """
    根据 jobid 获取 tasklist
    Returns:
        {
            'data': {
                'list': [
                    {
                        'task_namespace': u'',
                        'task_cmd': u"echo 'Hello World!' > helloWorld.out.txt;",
                        'ret_info': u'',
                        'job_id': 1,
                        'task_id': 1,
                        'ret_code': 0,
                        'task_priority': 0,
                        'task_cost': 0,
                        'task_mem': 2048,
                        'task_core_count': 1,
                        'c_time': datetime.datetime(2021, 4, 11, 17, 31, 59),
                        'task_label': u'easy_task1',
                        'task_dependencies': u'',
                        'task_status': u'finished',
                        'task_extra': u'{}',
                        'u_time': datetime.datetime(2021, 4, 11, 17, 31, 59)
                    },
                    {
                        ...
                    }
                ]
            }
        }
    """
    data = {}
    data_list = []
    record_list = model.Task.select().where(model.Task.job_id == int(job_id))
    for record in record_list:
        task_dict = shortcuts.model_to_dict(record)
        data_list.append(task_dict)

    data["list"] = data_list

    return retstat.OK, {"data": data}, [(__info, __version)]


@funcattr.api_download
def get_graph(req, job_id):
    """
    带参数请求例子

    Args:
        req             : (Object) Request
        job_id          : jobid
    Returns:
    """
    isinstance(req, Request)
    dot_file = os.path.join(config.BASE_DIR, "data/workflow_dot/{job_id}.dot".format(job_id=job_id))
    graph_file = os.path.join(config.BASE_DIR, "data/workflow_dot/{job_id}.png".format(job_id=job_id))
    gen_graph.write_dot_graph(job_id, dot_file)
    cmd = "dot -Tpng {dot_file} -o {graph_file}".format(
        dot_file=dot_file,
        graph_file=graph_file
    )
    shell_util.run(cmd)

    return retstat.OK, {"filename": graph_file, "is_download": True}, [(__info, __version)]
