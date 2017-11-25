__author__ = 'zhufree'
from django.conf.urls import url
from views import *

urlpatterns = [
    # Examples:
    url(r'^$', index),
    url(r'^p/(?P<id>\d+)/$', single_post),
    url(r'^topic/(?P<id>\d+)/$', show_topic),
    url(r'^post/$', post),

]

