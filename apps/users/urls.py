#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/9 13:46
# @Author  : Niyoufa
from django.urls import path
from users.views import *

urlpatterns = [
    path(r'login/', LoginView.as_view()),
    path(r'logout/', LogoutView.as_view()),
]