# -*-coding:utf-8-*-
from django.conf.urls import patterns, include, url
from room.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^bind/$', bind),
    url(r'^check/$', check),
    url(r'^login/$',  login),
    url(r'^reserve/$', reserv),
    url(r'^cancel/$', cancel),
    url(r'^roomid/$', roomid),
)