# -*- coding:utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.


class Message(models.Model):
    content = models.CharField(max_length=500, null=False, blank=False, default='')
    time = models.TimeField(auto_now=True)
    author = models.ForeignKey(User, related_name='user_messages')

    def __unicode__(self):
        return u'%s' % self.content

admin.site.register(Message)
