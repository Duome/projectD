# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from tags.models import Tag

class Link(models.Model):
    title = models.CharField(u'标题', max_length=100)
    address = models.CharField(u'地址', max_length=100)
    date = models.DateTimeField(u'时间')
    tag = models.ForeignKey(Tag)
