from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^register/$', register_),
    url(r'^login/$', login_),
    url(r'^logout/$', logout_),
    url(r'^register/api/', api_register_),
    url(r'^login/api/', api_login_),
    url(r'^logout/api/', api_logout_),
)
