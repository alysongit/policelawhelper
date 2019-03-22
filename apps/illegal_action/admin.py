#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 15:16
# @Author  : Niyoufa
import xadmin
from illegal_action.models import IllegalAction, \
    IllegalActionVersion, IllegalActionLawGist, IllegalactionSynonymword
from apps.admin import BaseAdmin


class IllegalActionAdmin(BaseAdmin):
    model_icon = 'fa fa-book'

    list_display = ["code", "name", "illegal_gist", "punish_gist", "score", "fine", "other_punish", "version"]
    list_display_links = ["code"]
    list_editable = []
    list_filter = ["version"]
    search_fields = ["code", "name"]
    show_detail_fields = ["name"]

    list_export = ["xls", "xml", "json"]
    list_export_fields= ["code", "name", "illegal_gist", "punish_gist", "score", "fine", "other_punish"]

    fields = ["version", "code", "name", "illegal_gist", "punish_gist",
              "score", "fine", "other_punish",
              "other_measure", "other_measure_gist", "force_measure", "force_measure_gist"]


class IllegalActionVersionAdmin(BaseAdmin):
    model_icon = 'fa fa-book'

    list_display = ["id", "province", "desc", "sort"]
    list_display_links = ["id"]
    list_editable = ["sort"]
    list_filter = ["province"]
    search_fields = ["province", "desc"]
    show_detail_fields = ["desc"]

    fields = ["province", "desc", "sort"]


class IllegalActionLawGistAdmin(BaseAdmin):
    model_icon = 'fa fa-book'

    list_display = ["id", "simple_name", "full_name", "version"]
    list_display_links = ["id"]
    list_editable = ["simple_name", "full_name"]
    list_filter = ["version"]
    search_fields = ["simple_name", "full_name"]
    show_detail_fields = ["simple_name"]

    fields = ["version", "simple_name", "full_name"]


class IllegalactionSynonymwordAdmin(BaseAdmin):
    model_icon = 'fa fa-book'

    list_display = ["word", "synonym_words"]
    search_fields = ("word", "synonym_words")
    list_display_links = ["word"]
    list_editable = ["synonym_words"]
    show_detail_fields = ["word"]

    fields = ["word", "synonym_words"]


xadmin.site.register(IllegalAction, IllegalActionAdmin)
xadmin.site.register(IllegalActionVersion, IllegalActionVersionAdmin)
xadmin.site.register(IllegalActionLawGist, IllegalActionLawGistAdmin)
xadmin.site.register(IllegalactionSynonymword, IllegalactionSynonymwordAdmin)