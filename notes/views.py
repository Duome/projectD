# -*- coding: utf-8 -*-

import json
from django.shortcuts import render
from models import *
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from tags.models import *
from django.contrib import messages


def get_notes(request):
    notes = Note.objects.all()
    tags = Tag.objects.all()
    if request.method == 'GET':
        return render(request, 'notes/list.html', locals())
    if request.method == 'POST' and request.POST.get('note_title'):
        note_id = request.POST.get('note_id', '')
        title = request.POST.get('note_title', '')
        text = request.POST.get('note_text', '')
        content = request.POST.get('note_content', '')
        tag = request.POST.get('note_tag')
        tag = Tag.objects.get(name=tag)
        created = datetime.now()
        modified = datetime.now()
        # add note
        try:
            Note.objects.get(title=title)
        except Note.DoesNotExist:
            Note.objects.create(title=title, text=text, content=content, created=created, modified=modified, tag=tag)
            messages.success(request, u"笔记'%s'添加成功！" % title)
        else:
            ret = 'error'
            messages.error(request, u"添加失败： 笔记'%s'已存在！" % title)
        return render(request, 'notes/list.html', locals())
    if request.method == 'POST' and request.POST.get('search_notes'):
        note_filter = request.POST.get('search_notes')
        notes_all = [note.title for note in Note.objects.all()]
        notes = []
        for note in notes_all:
            if note_filter in note:
                notes.append(note)
        return render(request, 'notes/list.html', locals())
    return render(request, 'notes/list.html', locals())

def ajax_show_note(request):
    note_id = request.GET.get('id', '')
    notes = Note.objects.filter(id=note_id).values()[0]
    title = notes['title']
    content = notes['content']
    created = datetime.strftime(notes['created'], '%Y-%m-%d %H:%M:%S')
    modified = datetime.strftime(notes['modified'], '%Y-%m-%d %H:%M:%S')
    tag_id = notes['tag_id']
    tag = Tag.objects.filter(id=tag_id).values()[0]['name']
    view = [note_id, title, content, created, modified, tag]
    return HttpResponse(json.dumps(view), content_type='application/json')


def ajax_edit_note(request):
    title = request.GET.get('title', '')
    note_id = request.GET.get('id', '')
    text = request.GET.get('text', '')
    content = request.GET.get('content', '')
    tag = request.GET.get('tag', '')
    tag = Tag.objects.get(name=tag)
    modified = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
    query_set = Note.objects.filter(title=title)
    if query_set and query_set[0].id != int(note_id):
        message = u"修改失败： 笔记'%s'已存在！" % title
        view = [message]
        return HttpResponse(json.dumps(view), content_type='application/json')
    else:
        note = Note.objects.get(id=note_id)
        note.title, note.text, note.content, note.modified, note.tag= title, text, content, modified, tag
        note.save()
        message = u"笔记'%s'修改成功！" % title
        note_id = note_id
        notes = Note.objects.filter(id=note_id).values()[0]
        title = notes['title']
        content = notes['content']
        created = datetime.strftime(notes['created'], '%Y-%m-%d %H:%M:%S')
        modified = datetime.strftime(notes['modified'], '%Y-%m-%d %H:%M:%S')
        tag_id = notes['tag_id']
        tag = Tag.objects.filter(id=tag_id).values()[0]['name']
        view = [note_id, title, content, created, modified, tag, message]
        return HttpResponse(json.dumps(view), content_type='application/json')

def delect_note(request):
    nli = request.GET.get('delete_note_id', '')
    Note.objects.filter(id=nli).delete()
    return HttpResponseRedirect(reverse('notes'))

