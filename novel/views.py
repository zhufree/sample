#-*- coding:utf-8 -*-
from django.shortcuts import render, Http404
from django.http import HttpResponse, HttpResponseRedirect
import json
from qiniu import Auth
from models import *
# Create your views here.


def index(request):
    novels = Novel.objects.all()
    return render(request, 'novel_index.html', {'novels': novels})


def show_novel_chapter(request, nid):
    cur_novel = Novel.objects.get(id=nid)
    chapters = cur_novel.has_chapters.all()
    return render(request, 'chapter_list.html', {'chapters': chapters})


def show_chapter_content(request, nid, cid):
    cur_chapter = Chapter.objects.get(id=cid)
    return render(request, 'chapter_content.html', {'chapter': cur_chapter})