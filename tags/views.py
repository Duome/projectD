# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse

from links.models import Link


from tags.models import Tag


def ajax_list_tag(request):
    tags = [tag.name for tag in Tag.objects.all()]
    return HttpResponse(json.dumps(tags), content_type='application/json')


def ajax_add_tag(request):
    name = request.GET.get('name', '')
    try:
        Tag.objects.get(name=name)
    except Tag.DoesNotExist:
        Tag.objects.create(name=name)
        return HttpResponse(u"标签'%s'添加成功！" % name)
    except Tag.MultipleObjectsReturned:
        return HttpResponse(u"添加失败： 标签'%s'存在多条重复记录！" % name)
    return HttpResponse(u"添加失败： '%s'标签已存在！" % name)


def ajax_delete_tag(request):
    name = request.GET.get('name', '')
    try:
        tag = Tag.objects.get(name=name)
    except Tag.DoesNotExist:
        return HttpResponse(u"删除失败： 标签'%s'不存在！" % name)
    except Tag.MultipleObjectsReturned:
        return HttpResponse(u"删除失败： 标签'%s'存在多条重复的记录！" % name)

    if Link.objects.filter(tag=tag):
        return HttpResponse(u"删除失败： 标签'%s'不为空，请先删除与该标签关联的链接！" % name)
    tag.delete()
    return HttpResponse(u"标签'%s'删除成功！" % name)
