#-*- coding:utf-8 -*-
from django.shortcuts import render, Http404
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.decorators import login_required
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


@login_required
def my_novels(request):
    novels = request.user.has_novels.all()
    return render(request, 'my_novels_list.html', {'novels': novels})


@login_required
def add_new_novel(request):
    if request.method == 'POST':
        new_novel = Novel(
            name=request.POST.get('name'),
            char_count=0,
            like_count=0
        )
        new_novel.save()
        new_novel.authors.add(request.user)
        novels = request.user.has_novels.all()
        return render(request, 'create_novel.html', {'novels': novels})
    else:
        novels = request.user.has_novels.all()
        #print novels
        return render(request, 'create_novel.html', {'novels': novels})


@login_required
def add_new_chapter(request):
    if request.method == 'POST':
        cur_novel = Novel.objects.get(id=request.POST.get('novel_id'))
        print cur_novel, request.POST.get('novel_id')
        new_chapter = Chapter(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            novel=cur_novel,
            author=request.user,
            char_count=len(request.POST.get('content')),
            like_count=0
        )
        new_chapter.save()
        return render(request, 'chapter_content.html', {'chapter': new_chapter})
    else:
        novels = request.user.has_novels.all()
        return render(request, 'create_chapter.html', {'novels': novels})
