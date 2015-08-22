# -*- coding:utf-8 -*-
from django.db import models
from django.contrib import admin
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20, null=False, default='')

    def __unicode__(self):
        return u'%s' % self.name


class Article(models.Model):
    title = models.CharField(max_length=30, null=True)
    content = models.TextField()
    time = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='has_articles')

    def __unicode__(self):
        return u'%s' % self.title


class Comment(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=20, null=False, blank=False, default='无名氏')
    content = models.TextField()
    article = models.ForeignKey(Article, related_name='has_comments', null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.content


admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Comment)
