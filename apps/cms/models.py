#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 14:03
# @Author  : Niyoufa
from django.db import models
from db.models import BaseModel, BaseTreeModel
from cms.fields import UnilineTextField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class CoverPicture(BaseModel):
    """内容封面图片"""

    name = models.CharField(max_length=255, verbose_name='图片名称')
    image = models.ImageField(upload_to='article_images/%Y-%m-%d %X', null=True, blank=True, verbose_name="图片地址")
    sort = models.IntegerField(default=0, verbose_name="顺序", help_text="值越小,越靠前")

    def __str__(self):
        format(self.image.url)
        return self.name

    class Meta(BaseModel.Meta):
        db_table = "cms_coverpicture"
        verbose_name = "图片"
        verbose_name_plural = "图片"


class Article(BaseModel):
    """内容表"""

    title = UnilineTextField(verbose_name="内容标题")
    content = RichTextUploadingField(verbose_name="内容文本")
    source = UnilineTextField(null=True, blank=True, verbose_name="来源")
    law_extract = models.BooleanField(default=False, verbose_name="是否进行法条解析")
    tab = models.ForeignKey("Tab", null=True, blank=True, on_delete=False, verbose_name="所属栏目")
    sort = models.IntegerField(default=0, verbose_name="顺序", help_text="值越小,越靠前")
    cover_pics = models.ManyToManyField(to="CoverPicture", blank=True, verbose_name="内容封面图片")

    def __str__(self):
        return self.title

    class Meta(BaseModel.Meta):
        db_table = "cms_article"
        verbose_name = "内容"
        verbose_name_plural = "内容"


class Tab(BaseTreeModel):
    """栏目表"""

    name = models.CharField(max_length=255, verbose_name="栏目名称")
    fixed = models.BooleanField(default=False, verbose_name="是否是固定栏目")
    parent = models.ForeignKey("self", null=True, blank=True, verbose_name="父栏目", related_name="children", on_delete=False)
    sort = models.IntegerField(default=0, verbose_name="顺序", help_text="值越小,越靠前")
    tab_type_choices = (
        (0, "常规"),
        (1, "直接内容"),
        (2, "自定义")
    )
    tab_type = models.IntegerField(choices=tab_type_choices, default=0, verbose_name="栏目类型", help_text="区分该栏目下的内容类型")

    def __str__(self):
        return self.name

    class Meta(BaseTreeModel.Meta):
        db_table = "cms_tab" #用于指定自定义数据库表名的
        verbose_name = "栏目"  #verbose_name的意思很简单，就是给你的模型类起一个更可读的名字
        verbose_name_plural = "栏目"#这个选项是指定，模型的复数形式是什么，如果不指定Django会自动在模型名称后加一个’s