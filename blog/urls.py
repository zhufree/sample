__author__ = 'zhufree'
from django.conf.urls import url
from .views import *

urlpatterns = [
    # Examples:
    url(r'^$', index),
    url(r'^article/(?P<id>\d+)/$', single_blog),
    url(r'^tag/(?P<id>\d+)/$', tag_blogs),
    url(r'^post/$', post),
]
