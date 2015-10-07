# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from book.views import *

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^historybook/$', historybook, name='历史记录'),
    url(r'^nowbook/$', nowbook, name='目前记录'),
    url(r'^renewall/$', renewall_, name='全部续借'),
    url(r'^renew/$', renew_, name='部分续借'),
    url(r'^search/$', search, name='搜索书籍'),
    url(r'^order/$', order, name='预约书籍'),
    url(r'^queryorder/$', queryorder_, name='查询预约书籍'),
    url(r'^deleteorder/$', deleteorder_, name='删除预约'),

)