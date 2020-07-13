#!/usr/bin/python
# coding=utf8
"""
# Author: wangbin34(meetbill)
# Created Time : 2020-07-13 22:50:44

# File Name: __init__.py
# Description:
    星河，统计数据

"""
from decimal import Decimal

from xlib.httpgateway import Request

from xlib import retstat
from xlib.middleware import funcattr
from xlib import db


__info = "xinghe"
__version = "1.0.1"


@funcattr.api
def get(req, name):
    """
    返回特定 name 的分组统计数据, 这个分组可以是时间，也可以是某个维度的分类

    Example:
    {
        'data': {
            'list': [{'value': 75.0, 'key': u'2020-06-19'}, {'value': 76.0, 'key': u'2020-06-20'}],
            'name': '自愈成功率',
            'title': '愈成功率统计(单位 %)'
            }
    }
    """
    isinstance(req, Request)
    data = {}

    # sql 语句中的 '%' 需要以 '%%' 替代
    xinghe_map = {
        "failover_total": {
            "sql": ("select date_format(c_time, '%%Y-%%m-%%d' ) days, count(*) count "
                    "from "
                    "qingnang_job  "
                    "where job_type = 'failover' "
                    "group by days;"
                    ),
            "name": "故障实例个数",
            "title": "故障实例统计(单位 个)"
        },
        "failover_success": {
            "sql": ("select date_format(c_time, '%%Y-%%m-%%d' ) days, count(*) count "
                    "from "
                    "qingnang_job "
                    "where job_type = 'failover' and job_state = 6000 "
                    "group by days;"
                    ),
            "name": "自愈成功个数",
            "title": "自愈成功实例统计(单位 个)"
        },
        "success_rate": {
            "sql": ("select Total.days,  Success.count/Total.count * 100 as success_rate "
                    "from  "
                    "(select date_format(c_time, '%%Y-%%m-%%d' ) days, count(*) count from qingnang_job  where job_type = 'failover' group by days) Total "
                    "left join "
                    "(select date_format(c_time, '%%Y-%%m-%%d' ) days, count(*) count from qingnang_job  where job_type = 'failover' and job_state = 6000 group by days) Success "
                    "on Total.days = Success.days;"
                    ),
            "name": "自愈成功率",
            "title": "自愈成功率统计(单位 %)"
        },
        "failover_idc_total": {
            "sql": ("select unit_idc result, count(1) n from qingnang_job where job_type = 'failover' group by result;"
                    ),
            "name": "故障实例所在机房统计",
            "title": "故障数"
        },
        "failover_idc_faild": {
            "sql": ("select unit_idc result, count(1) n from qingnang_job where job_type = 'failover' and job_state = 7000 group by result;"
                    ),
            "name": "自愈失败所在机房统计",
            "title": "自愈失败数"
        }
    }
    if name not in xinghe_map.keys():
        return retstat.ERR, {"data": data}, [(__info, __version)]

    data_list = []
    record_list = db.my_database.execute_sql(xinghe_map[name]["sql"]).fetchall()

    value_avg = 0
    value_sum = 0
    for record in record_list:
        item = {}
        item["key"] = record[0]
        # sql 语句返回的小数为 decimal 类型，无法直接转为 json, 在这里转为 float
        if isinstance(record[1], Decimal):
            item["value"] = float(record[1])
        else:
            item["value"] = record[1]

        data_list.append(item)
        value_sum = value_sum + item["value"]

    if len(record_list) != 0:
        value_avg = float(value_sum) / len(record_list)

    data["list"] = data_list
    data["name"] = xinghe_map[name]["name"]
    data["title"] = xinghe_map[name]["title"]
    data["avg"] = value_avg
    return retstat.OK, {"data": data}, [(__info, __version)]
