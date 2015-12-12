__author__ = 'zhufree'
from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'sample.views.home', name='home'),
    url(r'^$', index),
    url(r'n-(?P<nid>\d+)/$', show_novel_chapter),
    url(r'n-(?P<nid>\d+)/c-(?P<cid>\d+)/$', show_chapter_content),

)