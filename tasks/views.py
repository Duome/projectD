# -*- coding: utf-8 -*-

from django.shortcuts import render


def list_task(request):
    return render(request, 'tasks/list.html')