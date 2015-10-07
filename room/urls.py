# -*-coding:utf-8-*-
from django.conf.urls import patterns, include, url
from room.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^check/$',check),
    url(r'^login/$',login),
    url(r'^reserve/$',reserv),
    url(r'^cancel/$',cancel),
    url(r'^roomid/$',roomid),
    # Examples:
    # url(r'^$', 'work.views.home', name='home'),
    # url(r'^work/', include('work.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)