from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Novel(models.Model):
    name = models.CharField(max_length=30)
    authors = models.ManyToManyField(User, related_name='has_novels',)
    char_count = models.IntegerField()
    publish_time = models.DateTimeField(auto_now_add=True, default=timezone.now)
    update_time = models.DateTimeField(auto_now=True, default=timezone.now)
    like_count = models.IntegerField()
    def __unicode__(self):
        return u'%s' % self.name


class Chapter(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(blank=False, null=False)
    novel = models.ForeignKey(Novel, related_name='has_chapters')
    author = models.ForeignKey(User, related_name='has_chapters')
    char_count = models.IntegerField()
    publish_time = models.DateTimeField(auto_now_add=True, default=timezone.now)
    update_time = models.DateTimeField(auto_now=True, default=timezone.now)
    like_count = models.IntegerField()
    def __unicode__(self):
        return u'%s' % self.title

admin.site.register(Novel)
admin.site.register(Chapter)
