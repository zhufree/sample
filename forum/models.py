# -*- coding:utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s' % self.name


class Post(models.Model):
    author = models.ForeignKey(User, related_name='has_posts')
    title = models.CharField(max_length=30, blank=False)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, related_name='has_posts')
    last_reply_time = models.DateTimeField(auto_now=True)
    reply_count = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s' % self.title


class Reply(models.Model):
    author = models.ForeignKey(User, related_name='user_has_replys')
    content = models.TextField()
    floor_num = models.IntegerField(default=2)
    to_post = models.ForeignKey(Post, related_name='post_has_replys')
    to_reply = models.ForeignKey('self', related_name='reply_has_replys', null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.content


admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Reply)
