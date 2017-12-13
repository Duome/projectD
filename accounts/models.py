# encoding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=50)


class Role(models.Model):
    class Meta:
        permissions = (
            ("perm_account", u"用户管理权限"),
            ("perm_task", u"任务管理权限"),
            ("perm_link", u"收藏夹权限"),
            ("perm_note", u"笔记本权限"),
            ("perm_pay", u"记账簿权限"),
            ("perm_hdd", u"网盘权限"),
        )