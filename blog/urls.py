__author__ = 'zhufree'
from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', index),
    url(r'^article/(?P<id>\d+)/$', single_blog),
    url(r'^tag/(?P<id>\d+)/$', tag_blogs),

)
