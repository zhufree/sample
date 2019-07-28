# -*- coding:utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='has_chats',on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return u'%s' % self.content


admin.site.register(Chat)