# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from tags.models import Tag
# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=20, unique=True)
    text = models.CharField(max_length=30)
    content = models.CharField(max_length=1000000)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tag = models.ForeignKey(Tag)

# class History(models.Model):
#     information = models.CharField(max_length=100)
#     created = models.OneToOneField

