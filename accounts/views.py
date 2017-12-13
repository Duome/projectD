# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template.context import RequestContext
from django.db import IntegrityError
from django.contrib.auth.models import Permission
from .models import User


def list_user(request):
    users = User.objects.all()
    return render(request, 'accounts/list.html', locals())

def add_user(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        selects = request.POST.getlist('perm', '')

        try:
            user = User.objects.create(name=name, username=username, email=email, password=password)
            user.user_permissions.add()
            messages.success(request, u"用户'%s'添加成功！" % username)
            return HttpResponseRedirect(reverse('list_user'))
        except IntegrityError:
            messages.error(request, u"添加失败：用户'%s'已存在！" % username)
            return render(request, 'accounts/add.html', locals())

    perms = Permission.objects.filter(codename__istartswith='perm_')
    defaults = ['perm_task', 'perm_link', 'perm_note', 'perm_pay']
    return render(request, 'accounts/add.html', locals())

def update_user(request):
    username = request.GET.get('username', '')
    user = User.objects.get(username=username)
    name = user.name
    email = user.email
    password = user.password

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user.name = name
        user.email = email
        user.password = password

        user.save()
        messages.success(request, u"用户'%s'修改成功！" % username)

    return render_to_response('accounts/update.html', locals(), RequestContext(request))

def delete_user(request):
    username = request.GET.get('username', '')
    try:
        user = User.objects.get(username=username)
        user.delete()
        messages.success(request, u"用户'%s'删除成功！" % username)
    except User.DoesNotExist:
        messages.error(request, u"删除失败： 用户'%s'不存在！" % username)

    return HttpResponseRedirect(reverse('list_user'))
