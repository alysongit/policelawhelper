#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 19:52
# @Author  : Niyoufa
import logging
console_logger = logging.getLogger("console")

import re
from django.db.models import Q
from rest_framework.views import APIView
from libs import exceptionlib, handlerlib
from illegal_action.models import IllegalAction, IllegalActionVersion, \
    IllegalactionSynonymword, IllegalActionLawGist

synonym_words_dict = IllegalactionSynonymword.get_synonym_words_dict()
law_gist_dict = IllegalActionLawGist.get_law_gist_dict()

from illegal_action.cn2num import transform_to_int


class IllegalActionView(APIView):

    @exceptionlib.exception_handler
    def get(self, request):
        """
        获取栏目
        :param request:
        :return:
        """
        query_params = request.query_params
        page = int(query_params.get("page") or 1)
        page_size = int(query_params.get("page_size") or 10)

        province = query_params.get("province")
        if not province:
            raise exceptionlib.CustomException("省份参数不能为空")
        version = IllegalActionVersion.objects.filter(province=province).first()
        if not version:
            raise exceptionlib.CustomException("省份错误")

        keyword = query_params.get("keyword")
        if not keyword:
            raise exceptionlib.CustomException("检索词不能为空")
        else:
            keyword = keyword.strip()

        if keyword.isdigit():
            obj = IllegalAction.objects.filter(version=version, code=keyword).first()
            if obj:
                version = obj.version
                illegal_gist_text = obj.illegal_gist or ""
                punish_gist_text = obj.punish_gist or ""
                other_measure_gist_text = obj.other_measure_gist or ""
                force_measure_gist_text = obj.force_measure_gist or ""

                illegal_gist = illegal_gist_text and self.parse_law_gist(illegal_gist_text, version) or []
                punish_gist = punish_gist_text and self.parse_law_gist(punish_gist_text, version) or []
                other_measure_gist = other_measure_gist_text and self.parse_law_gist(other_measure_gist_text,
                                                                                     version) or []
                force_measure_gist = force_measure_gist_text and self.parse_law_gist(force_measure_gist_text,
                                                                                     version) or []
                data = [dict(
                    code=obj.code,
                    name=obj.name,
                    illegal_gist_text=illegal_gist_text,
                    illegal_gist=illegal_gist,
                    punish_gist_text=punish_gist_text,
                    punish_gist=punish_gist,
                    score=obj.score or 0,
                    fine=obj.fine or "",
                    other_punish=obj.other_punish or "",
                    other_measure=obj.other_measure or "",
                    other_measure_gist_text=other_measure_gist_text,
                    other_measure_gist=other_measure_gist,
                    force_measure=obj.force_measure or "",
                    force_measure_gist_text=force_measure_gist_text,
                    force_measure_gist=force_measure_gist,
                )]
                pager = IllegalAction.objects.count_page(1, page, page_size)
            else:
                data = []
                pager = IllegalAction.objects.count_page(0, page, page_size)
        else:
            queryset = IllegalAction.objects.filter(version=version)

            synonym_words = synonym_words_dict.get(keyword) or []
            synonym_words.append(keyword)
            console_logger.info(synonym_words)
            q = Q(name__contains=synonym_words[0])
            for word in synonym_words[1:]:
                q |= Q(name__contains=word)
            queryset = queryset.filter(q)

            data = []
            for obj in queryset[(page - 1) * page_size:page * page_size]:
                version = obj.version
                illegal_gist_text = obj.illegal_gist or ""
                punish_gist_text = obj.punish_gist or ""
                other_measure_gist_text = obj.other_measure_gist or ""
                force_measure_gist_text = obj.force_measure_gist or ""

                illegal_gist = illegal_gist_text and self.parse_law_gist(illegal_gist_text, version) or []
                punish_gist = punish_gist_text and self.parse_law_gist(punish_gist_text, version) or []
                other_measure_gist = other_measure_gist_text and self.parse_law_gist(other_measure_gist_text,
                                                                                    version) or []
                force_measure_gist = force_measure_gist_text and self.parse_law_gist(force_measure_gist_text,
                                                                                    version) or []
                data.append(dict(
                    code=obj.code,
                    name=obj.name,
                    illegal_gist_text = illegal_gist_text,
                    illegal_gist=illegal_gist,
                    punish_gist_text = punish_gist_text,
                    punish_gist=punish_gist,
                    score=obj.score or 0,
                    fine=obj.fine or "",
                    other_punish=obj.other_punish or "",
                    other_measure=obj.other_measure or "",
                    other_measure_gist_text = other_measure_gist_text,
                    other_measure_gist=other_measure_gist,
                    force_measure=obj.force_measure or "",
                    force_measure_gist_text = force_measure_gist_text,
                    force_measure_gist=force_measure_gist,
                ))
            pager = IllegalAction.objects.count_page(queryset.count(), page, page_size)

        result = handlerlib.init_response_data()
        result["data"] = data
        result["pager"] = pager
        response = handlerlib.JSONResponse(result)
        return response

    def parse_law_gist(self, text, version):
        regex = r"《[\u4e00-\u9fa5]+》第[零一二三四五六七八九十百千万0-9]+条" \
                r"(?:第[零一二三四五六七八九十百千万0-9]+款)?" \
                r"(?:第[零一二三四五六七八九十百千万0-9]+项)?"
        regex_extract = r"^《(?P<simple_name>[\u4e00-\u9fa5]+)》第(?P<clause>[零一二三四五六七八九十百千万0-9]+)条"
        law_gist = []
        for s in re.findall(regex, text):
            matched = re.search(regex_extract, s)
            groupdict = matched.groupdict()
            simple_name = groupdict.get("simple_name")
            clause = groupdict.get("clause")
            if clause.isdigit():
                clause = int(clause)
            else:
                clause = transform_to_int(clause)
            law_gist.append(dict(
                text = s,
                simple_name=simple_name,
                full_name=(law_gist_dict.get(version.id) or {}).get(simple_name) or simple_name,
                clause=clause,
            ))
        return law_gist