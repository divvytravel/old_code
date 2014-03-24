# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from trip.views import TripFilterFormView
from trip.views import index_view

from postman.forms import AnonymousWriteForm
from postman_custom.views import AjaxWriteView
from postman_custom.forms import WriteFormHideRecipients


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index_view, name='home'),
    url(r'^api/', include('api.urls')),
    # url(r'^$', TripFilterFormView.as_view(), name='home'),
    url(r'^trip/', include("trip.urls")),
    url(r'^geo/', include("geo.urls")),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("users.urls", namespace="users")),
    url(r'^accounts/', include('social_auth.urls')),

    url(r'^messages/write/(?:(?P<recipients>[\w.@+-:]+)/)?$',
        AjaxWriteView.as_view(
            form_classes=(WriteFormHideRecipients, AnonymousWriteForm)),
        name='postman_write'),
    url(r'^messages/', include('postman.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

# if settings.OPENSHIFT_GEAR_NAME is not None:
#     urlpatterns += patterns('django.contrib.st'
#                             'aticfiles.views',
#         url(r'^static/(?P<path>.*)$', 'serve',
#             {'document_root': settings.STATIC_ROOT, 'insecure': True}),
#         url(r'^media/(?P<path>.*)$', 'serve',
#             {'document_root': settings.MEDIA_ROOT, 'insecure': True}),
#     )
