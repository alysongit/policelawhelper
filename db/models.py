#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/5 16:37
import math
from bson import ObjectId
from django.db import models
from mptt.models import MPTTModel
from db.managers import TreeManager


class BaseManager(models.Manager):

    def gen_objectid(self, oid=None):
        if oid:
            ObjectId(oid)
            object_id = oid
        else:
            object_id = str(ObjectId())
        return object_id

    def create(self, **kwargs):
        id = kwargs.get("id")
        if not id:
            id = self.gen_objectid(kwargs.get("id"))

        kwargs.update(dict(
            id=id,
        ))
        return super(BaseManager, self).create(**kwargs)

    def tree(self, objs):
        tree = []
        for obj in objs:
            tree.append(obj.name)
            children = obj.children.all()
            if len(children) > 0:
                tree.append(self.tree(obj.children.all()))
        return tree

    def bulk_create(self, objs, batch_size=None):
        for obj in objs:
            if not obj.id:
                obj.id = self.gen_objectid()
        return super(BaseManager, self).bulk_create(objs, batch_size)

    # 计算分页信息
    def count_page(
            self,
            length,
            page,
            page_size,
            page_show=10):
        if page:
            page = int(page)
        else:
            page = 1

        if page_size:
            page_size = int(page_size)
        else:
            page_size = 10

        length = int(length)
        if length == 0:
            return {"enable": False,
                    "page_size": page_size,
                    "skip": 0}
        max_page = int(math.ceil(float(length) / page_size))
        page_num = int(math.ceil(float(page) / page_show))
        pages = list(range(1, max_page + 1)
                     [((page_num - 1) * page_show):(page_num * page_show)])
        skip = (page - 1) * page_size
        if page >= max_page:
            has_more = False
        else:
            has_more = True
        pager = {
            "page_size": page_size,
            "max_page": max_page,
            "pages": pages,
            "page_num": page_num,
            "skip": skip,
            "page": page,
            "enable": True,
            "has_more": has_more,
            "total": length,
        }
        return pager

class BaseModel(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name="ID") # 支持分布式系统的全局唯一ID，使用ObjectId生成
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    update_user = models.CharField(max_length=255, verbose_name="修改用户")
    is_enable = models.BooleanField(default=True, verbose_name="是否删除")

    objects = BaseManager()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not hasattr(self, "id") or not self.id:
            self.id = self.__class__.objects.gen_objectid()
        return super(BaseModel, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True


class BaseTreeModel(MPTTModel):
    id = models.CharField(max_length=255, primary_key=True, verbose_name="ID")  # 支持分布式系统的全局唯一ID，使用ObjectId生成
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    update_user = models.CharField(max_length=255, verbose_name="修改用户")
    is_enable = models.BooleanField(default=True, verbose_name="是否删除")

    objects = TreeManager()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not hasattr(self, "id") or not self.id:
            self.id = self.__class__.objects.gen_objectid()
        return super(BaseTreeModel, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True # 这个属性是定义当前的模型类是不是一个抽象类。所谓抽象类是不会对应数据库表的。