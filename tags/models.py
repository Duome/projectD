# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Tag(models.Model):
    name = models.CharField(u'名称', max_length=30)
