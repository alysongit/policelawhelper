#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/4 13:05
# @Author  : Niyoufa
# @Site    : 
# @File    : test.py.py
# @Software: PyCharm

from django.http import HttpResponse

from rest_framework.renderers import JSONRenderer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, result={}, **kwargs):
        result = result or init_response_data()
        content = JSONRenderer().render(result)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# 初始化返回参数
def init_response_data():
    result = {'code': 200, 'msg': '返回成功'}
    return result


# 重置返回参数
def reset_response_data(info, code=400):
    result = {'code': code, 'msg': str(info)}
    return result
