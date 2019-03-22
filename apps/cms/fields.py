#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 14:01
# @Author  : Niyoufa
from django.db import models
from django import forms
from django.forms.widgets import Textarea


class UnilineTextField(models.TextField):

    def formfield(self, **kwargs):
        return models.Field.formfield(self, UnilineTextareaForm , **kwargs)

class UnilineTextareaForm(forms.CharField):
    widget = Textarea

    def widget_attrs(self, widget):
        """
        Given a Widget instance (*not* a Widget class), return a dictionary of
        any HTML attributes that should be added to the Widget, based on this
        Field.
        """
        return {'cols': '1', 'rows': '1'}