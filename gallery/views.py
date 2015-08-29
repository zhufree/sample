#-*- coding:utf-8 -*-
from django.shortcuts import render, Http404
from django.http import HttpResponse, HttpResponseRedirect
import json
from qiniu import Auth
from models import *
from privatesettings import *# 关于七牛的key信息
# Create your views here.


def uptoken(request):
    q = Auth(ACCESS_KEY, SECRET_KEY)
    token = q.upload_token(BUCKET_NAME)
    data = {'uptoken': token}
    return HttpResponse(json.dumps(data), content_type="application/json")


def index(request):
    photos = Photo.objects.all().order_by('like_count')
    return render(request, 'gallery_index.html',{'photos': photos})


def post(request):
    if request.method == 'POST':
        if request.POST.get('post_type') == 'post_photo':
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
    else:
        raise Http404