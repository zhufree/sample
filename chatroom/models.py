# -*- coding:utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.


class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='has_chats')
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True, null=True)


    def __unicode__(self):
        return u'%s' % self.content


admin.site.register(Chat)