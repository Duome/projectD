# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    return HttpResponseRedirect(reverse('list_task'))

def about(request):
    return render(request, 'footer/about.html')

def contact(request):
    return render(request, 'footer/contact.html')

def reward(request):
    return render(request, 'footer/reward.html')