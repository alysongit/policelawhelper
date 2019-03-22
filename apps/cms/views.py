#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 17:56
# @Author  : Niyoufa
import logging
console_logger = logging.getLogger("console")

from rest_framework.views import APIView
from libs import exceptionlib, handlerlib
from cms.models import Tab, Article

from cms.article_parse.parse_para.parsers import ArticleParaParser
article_para_parser = ArticleParaParser()


class TabView(APIView):

    @exceptionlib.exception_handler
    def get(self, request):
        """
        获取栏目
        :param request:
        :return:
        """
        data = []
        root_nodes = Tab.objects.root_nodes().order_by("sort")
        self.build_tree(root_nodes, data)
        result = handlerlib.init_response_data()
        result["data"] = data
        response = handlerlib.JSONResponse(result)
        return response

    def build_tree(self, root_nodes, data):
        for index, node in enumerate(root_nodes):
            obj = dict(
                id=node.id,
                name=node.name,
                parent=node.parent and node.parent.id,
                level = node.level,
                fixed=node.fixed,
                sort=node.sort,
                tab_type=node.tab_type,
                children=[]
            )
            data.append(obj)
            children = node.get_children().order_by("sort")
            if children:
                self.build_tree(children, obj["children"])


class ArticleView(APIView):

    @exceptionlib.exception_handler
    def get(self, request):
        """
        查询栏目文章
        :param request:
        :return:
        """
        queryset = Article.objects.all()

        query_params = request.query_params

        tab_id = query_params.get("tab_id")
        if tab_id:
            queryset = queryset.filter(tab_id=tab_id).order_by("sort")

        page = query_params.get("page") or 1
        page_size = query_params.get("page_size") or 10
        queryset = queryset[(page-1)*page_size:page*page_size]

        data = []
        for obj in queryset:
            data.append(dict(
                id = obj.id,
                title = obj.title,
                content = obj.content,
                source = obj.source,
                sort = obj.sort,
                cover_pics = [dict(
                    name = pic.name,
                    url = pic.image.url
                ) for pic in obj.cover_pics.all().order_by("sort")],
                tab_name = obj.tab.name,
                time = str(obj.update_time).split(" ")[0],
                paras = self.parse_para(obj.content),
            ))

        result = handlerlib.init_response_data()
        result["data"] = data
        response = handlerlib.JSONResponse(result)
        return response

    def parse_para(self, content):
        paras = article_para_parser.parse(content)
        return paras