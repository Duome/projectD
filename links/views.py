# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils import timezone

from tags.models import Tag
from links.models import Link


def list_link(request):
    if request.method == 'POST':
        link_id = request.POST.get('update-id', '')
        title = request.POST.get('update-title', '') if link_id else request.POST.get('add-title', '')
        address = request.POST.get('update-address', '') if link_id else request.POST.get('add-address', '')
        tag_name = request.POST.get('update-tag', '') if link_id else request.POST.get('add-tag', '')
        tag = Tag.objects.get(name=tag_name)
        date = timezone.now()
        if link_id:
            # update link
            query_set = Link.objects.filter(title=title)
            if query_set and query_set[0].id != int(link_id):
                messages.error(request, u"修改失败： 链接'%s'已存在！" % title)
            else:
                link = Link.objects.get(id=link_id)
                link.title, link.address, link.tag, link.date = title, address, tag, date
                link.save()
                messages.success(request, u"链接'%s'修改成功！" % title)
        else:
            # add link
            try:
                Link.objects.get(title=title)
            except Link.DoesNotExist:
                Link.objects.create(title=title, address=address, tag=tag, date=date)
                messages.success(request, u"链接'%s'添加成功！" % title)
            else:
                ret = 'error'
                messages.error(request, u"添加失败： 链接'%s'已存在！" % title)
    # list link
    tags = Tag.objects.all()
    links = Link.objects.all()
    return render(request, 'links/list.html', locals())


def delete_link(request):
    title = request.GET.get('delete-title', '')
    try:
        link = Link.objects.get(title=title)
    except Link.DoesNotExist:
        messages.error(request, u"删除失败： 链接'%s'不存在！" % title)
    else:
        link.delete()
        messages.success(request, u"链接'%s'删除成功！" % title)
    return HttpResponseRedirect(reverse('list_link'))
