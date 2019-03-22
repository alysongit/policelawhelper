#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 12:51
# @Author  : Niyoufa
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django_bulk_update.manager import BulkUpdateManager
from users.models import Account


class Command(BaseCommand):
    """导入交警权限"""

    def handle(self, *args, **options):
        polices = Account.objects.filter(username__startswith="police").all()
        group = Group.objects.get(name="交警")
        for police in polices.iterator():
            print(police)
            police.groups.add(group)
            police.save()