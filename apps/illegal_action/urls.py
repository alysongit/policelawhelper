#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 19:59
# @Author  : Niyoufa
from django.urls import path
from illegal_action.views import *

urlpatterns = [
    path(r'illegalaction/', IllegalActionView.as_view()),
]