from django.conf.urls import url
from views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'sample.views.home', name='home'),
    url(r'^$', index),
    url(r'^post/$', post),

]
