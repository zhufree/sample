__author__ = 'zhufree'
from django.conf.urls import url
from .views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'sample.views.home', name='home'),
    url(r'^$', index),
    url(r'n-(?P<nid>\d+)/$', show_novel_chapter),
    url(r'n-(?P<nid>\d+)/c-(?P<cid>\d+)/$', show_chapter_content),
    url(r'add_new_novel/$', add_new_novel),
    url(r'add_new_chapter/$', add_new_chapter),
    url(r'mynovels/$', my_novels),
]
