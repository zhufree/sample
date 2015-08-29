from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^register/', register_),
    url(r'^login/', login_),
    url(r'^logout/', logout_),
)
