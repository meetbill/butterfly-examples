#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-10-28 00:31:43

# File Name: __init__.py
# Description:
    Redis 资源计算器

"""
__info__ = "meetbill"
__version__ = "1.0.1"

from xlib.httpgateway import Request
from xlib import retstat
def redis(req):
    """
    输出 redis 资源计算器
    """
    isinstance(req, Request)
    with open("./templates/redis.html") as  f:
        context = f.read()
    return retstat.HTTP_OK, context,[("Content-Type","text/html")]
