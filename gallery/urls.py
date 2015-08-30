__author__ = 'zhufree'
from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', index),
    url(r'^uptoken/$', uptoken),
    url(r'^p/(?P<pid>\d+)/$', show_photo),
    url(r'^t/(?P<tid>\d+)/$', show_tag),
    url(r'^post/$', post),

)
