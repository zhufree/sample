from django.conf.urls import include, url
from django.contrib import admin

from usersys.views import *

urlpatterns = [
    # Examples:
    url(r'^$', index, name='homepage'),
    url(r'^msg/', include('msgpad.urls')),
    url(r'^accounts/', include('usersys.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^forum/', include('forum.urls')),
    url(r'^gallery/', include('gallery.urls')),
    url(r'^chatroom/', include('chatroom.urls')),
    # url(r'^tieba/', include('tieba.urls')),
    url(r'^eat/', include('eat.urls')),
    url(r'^novel/', include('novel.urls')),
    url(r'^about/$', about),
    url(r'^projects/$', projects),

    url(r'^admin/', admin.site.urls),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve'),
]
