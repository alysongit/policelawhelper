#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 12:26
# @Author  : Niyoufa
from xadmin.filters import BaseFilter
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TabFilter(BaseFilter):
    title = "栏目筛选"
    parameter_name = ''

    lookup_formats = {'exact': '%s__exact'}

    def has_output(self):
        return True

    def choices(self):
        yield {
            'selected': self.lookup_exact_val is '',
            'query_string': self.query_string({}, [self.lookup_exact_name]),
            'display': _('All')
        }
        for lookup, title in self.field.flatchoices:
            yield {
                'selected': True,
                'query_string': self.query_string({self.lookup_exact_name: lookup}),
                'display': title,
            }

    def do_filte(self, queryset):
        return queryset