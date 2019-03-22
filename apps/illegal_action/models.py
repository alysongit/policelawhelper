#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 14:52
# @Author  : Niyoufa
from collections import defaultdict
from django.db import models
from db.models import BaseModel

class IllegalActionVersion(BaseModel):
    province = models.CharField(max_length=255, verbose_name="省份")
    desc = models.CharField(max_length=255, verbose_name="版本描述")
    sort = models.IntegerField(default=0, verbose_name="顺序", help_text="值越小,越靠前")

    def __str__(self):
        return "{} {}".format(self.province, self.desc)

    class Meta(BaseModel.Meta):
        db_table = "illegalaction_version"
        verbose_name = "违法行为版本"
        verbose_name_plural = verbose_name

        unique_together = (
            ("province", "desc")
        )


class IllegalAction(BaseModel):
    version = models.ForeignKey("IllegalActionVersion", on_delete=False, verbose_name="版本")
    code = models.CharField(max_length=255, verbose_name="违法行为代码")
    name = models.TextField(verbose_name="违法行为名称")
    illegal_gist = models.TextField(null=True, blank=True, verbose_name="违法依据")
    punish_gist = models.TextField(null=True, blank=True, verbose_name="惩罚依据")
    score = models.IntegerField(default=0, verbose_name="记分")
    fine = models.CharField(max_length=255, null=True, blank=True, verbose_name="罚金")
    other_punish = models.TextField(null=True, blank=True, verbose_name="其他处罚")
    other_measure = models.TextField(null=True, blank=True, verbose_name="其他措施")
    other_measure_gist = models.TextField(null=True, blank=True, verbose_name="其他措施依据")
    force_measure = models.TextField(null=True, blank=True, verbose_name="强制措施")
    force_measure_gist = models.TextField(null=True, blank=True, verbose_name="强制措施依据")

    def __str__(self):
        return "{} {} {}".format(self.version, self.code, self.name)

    class Meta(BaseModel.Meta):
        db_table = "illegalaction"
        verbose_name = "违法行为代码"
        verbose_name_plural = verbose_name

        unique_together = (
            ("version", "code")
        )


class IllegalActionLawGist(BaseModel):
    version = models.ForeignKey("IllegalActionVersion", on_delete=False, verbose_name="版本")
    simple_name = models.CharField(max_length=255, verbose_name="法律简称")
    full_name = models.CharField(max_length=255, verbose_name="法律全称")

    def __str__(self):
        return self.simple_name

    class Meta(BaseModel.Meta):
        db_table = "illegalaction_lawgist"
        verbose_name = "法律依据映射表"
        verbose_name_plural = verbose_name

    @classmethod
    def get_law_gist_dict(cls):
        objs = cls.objects.all()
        law_gist_dict = defaultdict(dict)
        for obj in objs:
            version = obj.version
            law_gist_dict[version.id].update({obj.simple_name:obj.full_name})
        return law_gist_dict


class IllegalactionSynonymword(BaseModel):
    word = models.CharField(max_length=255, unique=True, verbose_name="检索词")
    synonym_words = models.TextField(verbose_name="同义词组")

    class Meta(BaseModel.Meta):
        db_table = "illegalaction_synonymword"
        verbose_name = "同义词映射表"
        verbose_name_plural = "同义词映射表"

    @classmethod
    def get_synonym_words_dict(cls):
        objs = cls.objects.all()
        synonym_words_dict = defaultdict(list)
        for obj in objs:
            word = obj.word.strip()
            synonym_words = [word for word in obj.synonym_words.split("\n") if word and word.strip()]
            synonym_words_dict[word].extend(list(set(synonym_words)))
        return synonym_words_dict