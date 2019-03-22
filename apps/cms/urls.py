#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 17:59
# @Author  : Niyoufa
from django.urls import path
from cms.views import *

urlpatterns = [
    path(r'tab/', TabView.as_view()),
    path(r'article/', ArticleView.as_view()),
]