#-*- coding:utf-8 -*-
from django.shortcuts import render, Http404
from django.http import HttpResponse, HttpResponseRedirect
import json
from qiniu import Auth
from models import *
# 关于七牛的key信息
from private_settings import *
# Create your views here.


def uptoken(request):
    q = Auth(ACCESS_KEY, SECRET_KEY)
    token = q.upload_token(BUCKET_NAME)
    data = {'uptoken': token}
    return HttpResponse(json.dumps(data), content_type="application/json")


def index(request):
    photos = Photo.objects.all().order_by('like_count')
    return render(request, 'gallery_index.html',{'photos': photos})


def show_tag(request, tid):
    cur_tag = Tag.objects.get(id=tid)
    photos = cur_tag.tag_has_photos.all()
    return render(request, 'show_tag.html', {'tag':cur_tag, 'photos':photos})


def show_photo(request,pid):
    cur_photo = Photo.objects.get(id=pid)
    return render(request, 'show_photo.html', {'photo': cur_photo})


def post(request):
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        if post_type == 'post_photo':
            new_photo = Photo.objects.create(
                name=request.POST.get('name'),
                link=request.POST.get('link'),
                description=request.POST.get('description'),
                up_loader=request.user,
                like_count=0,
                )
            tags=request.POST.get('tags').split()
            if tags:
                for tagname in tags:
                    new_tag,dummy = Tag.objects.get_or_create(name=tagname)
                    new_tag.count += 1
                    new_tag.save()
                    new_photo.tags.add(new_tag)#add tag to new_photo
            new_photo.save()
            return HttpResponseRedirect('/gallery/')
        elif post_type == 'photo_comment':
            photo_id = request.POST.get('photo_id')
            new_comment = Comment.objects.create(
                content=request.POST.get('content'),
                author=request.user,
                photo=Photo.objects.get(id=photo_id)
            )
            new_comment.save()
            return HttpResponseRedirect('/gallery/p/%s/' % photo_id)
    else:
        raise Http404