#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 15:30
# @Author  : Niyoufa
import os
import xlrd
from django.conf import settings
from django.core.management.base import BaseCommand
from illegal_action.models import IllegalAction, IllegalActionVersion


class Command(BaseCommand):
    """导入交警信息"""

    def handle(self, *args, **options):
        self.import_from_es()
        self.import_from_xlsx()

    def import_from_es(self):
        import json
        import requests
        url = "http://super:superuser@hotbkes.aegis-info.com:9255/traffic_illegal_action/_search"
        res = requests.post(url, json={"size": 1000})
        hits = json.loads(res.content.decode())["hits"]["hits"]
        data = [hit["_source"] for hit in hits]
        version_obj = IllegalActionVersion.objects.filter(province="江苏省").first()
        objs = []
        code_set = set()
        for doc in data:
            code = doc["code"]
            if not code in code_set:
                obj = IllegalAction(
                    version = version_obj,
                    code = code,
                    name = doc["name"],
                    illegal_gist = doc.get("illegalGist"),
                    punish_gist = doc.get("publishGist"),
                    score = doc.get("score") or 0,
                    fine = doc.get("fine"),
                    other_measure = doc.get("otherMeasure")
                )
                objs.append(obj)
                code_set.add(code)
            else:
                print(code)
        IllegalAction.objects.bulk_create(objs)

    def import_from_xlsx(self):
        file_path = os.path.join(settings.BASE_DIR, "data/code.xlsx")
        data = xlrd.open_workbook(file_path)
        table = data.sheets()[0]
        nrows = table.nrows

        version_obj = IllegalActionVersion.objects.filter(province="湖北省").first()
        objs = []
        code_set = set()
        for i in range(2, nrows):
            try:
                table_row_values = table.row_values(i)
                code = str(int(table_row_values[0])).strip()
                name = table_row_values[1].strip()
                illegal_gist = table_row_values[2].strip()
                punish_gist = table_row_values[3].strip()
                score = int(table_row_values[4] or 0)
                fine = str(table_row_values[5]).strip()
                other_punish = table_row_values[6].strip()
                force_measure = table_row_values[7].strip()
                force_measure_gist = table_row_values[8].strip()
                other_measure = table_row_values[9].strip()
                other_measure_gist = table_row_values[10].strip()
            except:
                print(table_row_values)
                continue

            if not code in code_set:
                obj = IllegalAction(
                    version = version_obj,
                    code = code,
                    name = name,
                    illegal_gist = illegal_gist,
                    punish_gist = punish_gist,
                    score = score,
                    fine = fine,
                    other_punish = other_punish,
                    force_measure = force_measure,
                    force_measure_gist = force_measure_gist,
                    other_measure = other_measure,
                    other_measure_gist = other_measure_gist
                )
                objs.append(obj)
                code_set.add(code)
            else:
                print(code)
        IllegalAction.objects.bulk_create(objs)
