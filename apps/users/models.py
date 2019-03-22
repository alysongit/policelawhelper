#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 9:44
# @Author  : Niyoufa
from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):

    gender_choices = (
        ('male','男'),
        ('female','女')
    )

    police_code = models.CharField('警号', unique=True, max_length=255, default='')
    nick_name = models.CharField('昵称', max_length=50, null=True, blank=True, default='')
    birthday = models.DateField('生日', null=True, blank=True)
    gender = models.CharField('性别', max_length=10, choices=gender_choices, default='male')
    adress = models.CharField('地址', max_length=100, null=True, blank=True, default='')
    mobile = models.CharField('手机号', max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='images/%Y%m', null=True, blank=True, default='images/default_avatar.png', max_length=100, verbose_name="头像")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class PoliceGroup(models.Model):
    name = models.CharField('名称', unique=True, max_length=255, default='')
    code = models.CharField('代码', unique=True, max_length=255, default='')

    class Meta:
        verbose_name = '警队'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PoliceType(models.Model):
    name = models.CharField('名称', max_length=255, default='')

    class Meta:
        verbose_name = '警种'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Police(models.Model):
    name = models.CharField('姓名', max_length=255, default='')
    police_code = models.CharField('警号', unique=True, max_length=255, default='')
    police_type = models.ForeignKey("PoliceType", null=True, blank=True, verbose_name="警种", on_delete=False)
    police_group = models.ForeignKey("PoliceGroup", verbose_name="警队", on_delete=False)
    imei = models.CharField('物理串号', max_length=255, default='')

    class Meta:
        verbose_name = '警察'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
