__author__ = 'zhufree'
from django.conf.urls import url
from .views import *

urlpatterns = [
    # Examples:
    url(r'^$', index),
    url(r'^add_rest/$', add_rest),
    url(r'^roll/$', roll),
]
