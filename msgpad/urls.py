from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'sample.views.home', name='home'),
    url(r'^$', index),

)
