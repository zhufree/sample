__author__ = 'zhufree'
from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', index),
    url(r'^add_rest/$', add_rest),
    url(r'^roll/$', roll),

)