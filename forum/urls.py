__author__ = 'zhufree'
from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', index),
    url(r'^p/(?P<id>\d+)/$', single_post),
    #url(r'^tag/(?P<id>\d+)/$', tag_blogs),
    url(r'^post/$', post),

)

