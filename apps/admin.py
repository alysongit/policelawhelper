#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 10:32
# @Author  : Niyoufa
from users.models import Account


class BaseAdmin(object):
    list_per_page = 10
    ordering = ["-id"]
    refresh_times = (60,)
    list_display_links = ["id"]
    free_query_filter = True

    def last_update_user_name(self, obj):
        update_user = obj.update_user
        username = "未知"
        if update_user:
            user = Account.objects.filter(username=update_user).first()
            username = user.first_name
        return username
    last_update_user_name.short_description = "最后修改用户"

    def save_models(self):
        self.new_obj.update_user = self.user.username
        self.new_obj.save()
        flag = self.org_obj is None and 'create' or 'change'
        self.log(flag, self.change_message(), self.new_obj)

    def last_update_time(self, obj):
        update_time = obj.update_time
        print(update_time)
        if update_time:
            update_time = str(update_time).split(".")[0]
        return update_time
    last_update_time.short_description = "最后修改时间"
