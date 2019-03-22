#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 17:58
# @Author  : Niyoufa
import os
import xlrd
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from users.models import PoliceGroup, Police, Account


class Command(BaseCommand):
    """导入交警信息"""

    def handle(self, *args, **options):
        data = xlrd.open_workbook(os.path.join(settings.BASE_DIR, 'data/police.xlsx'))
        table = data.sheets()[0]
        nrows = table.nrows
        police_group_set = set()
        police_groups = []
        police_code_set = set()
        polices = set()
        for i in range(1, nrows):
            table_row_values = table.row_values(i)
            print(table_row_values)

            group_name = table_row_values[2]
            group_code = table_row_values[1]
            if not group_code in police_group_set:
                police_group_set.add(group_code)
                police_groups.append((group_name, group_code))

            name = table_row_values[4]
            police_code = table_row_values[3]
            imei = table_row_values[5]
            if not police_code in police_code_set:
                police_code_set.add(police_code)
                polices.add((name, police_code, imei, group_code))

        try:
            objs = PoliceGroup.objects.bulk_create([PoliceGroup(
                name = police_group[0],
                code = police_group[1]
            ) for police_group in police_groups])
        except Exception as err:
            print(err.args)
            objs = PoliceGroup.objects.all()

        police_group_dict = {}
        for obj in objs:
            police_group_dict[obj.code] = obj

        try:
            polices = Police.objects.bulk_create([Police(
                name = police[0],
                police_code = police[1],
                imei = police[2],
                police_group = police_group_dict[police[3]]
            ) for police in polices])
        except Exception as err:
            print(err.args)
            polices = Police.objects.all()

        created_objs = Account.objects.filter(police_code__in=police_code_set).all()
        created_police_codes = [obj.police_code for obj in created_objs]
        uncreate_objs = [obj for obj in polices if not obj.police_code in created_police_codes]
        accounts = [Account(
            police_code = obj.police_code,
            username = "police%s"%obj.police_code,
            first_name = obj.name,
            is_staff = True,
            is_active = True,
            password = make_password("police%s"%obj.police_code),
        ) for obj in uncreate_objs]
        Account.objects.bulk_create(accounts)
