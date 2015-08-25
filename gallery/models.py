# -*- coding:utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False)


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, related_name='has_comments')


class Photo(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    link = models.URLField(unique=True, blank=False,null=False)
    description = models.TextField(null=True)
    up_loader = models.ForeignKey(User, related_name='has_photos')
    time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='has_photos')
    like_count = models.IntegerField(default=0)


admin.site.register(Tag)
admin.site.register(Photo)
