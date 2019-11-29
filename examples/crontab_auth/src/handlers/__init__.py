#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-07-21 09:31:43

# File Name: 输出首页.py
# Description:

"""
__info__ = "meetbill"
__version__ = "1.0.1"

from xlib.httpgateway import Request
from xlib import retstat
def main(req):
    """
    """
    isinstance(req, Request)
    with open("./templates/index.html") as  f:
        context = f.read()
    return retstat.HTTP_OK, context
