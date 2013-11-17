# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from trip.views import TripFilterFormView

from postman.forms import AnonymousWriteForm
from postman.views import WriteView
from postman_custom.forms import WriteFormHideRecipients


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TripFilterFormView.as_view(), name='home'),
    url(r'^trip/', include("trip.urls")),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("users.urls", namespace="users")),
    url(r'^accounts/', include('social_auth.urls')),

    url(r'^messages/write/(?:(?P<recipients>[\w.@+-:]+)/)?$',
        WriteView.as_view(
            form_classes=(WriteFormHideRecipients, AnonymousWriteForm)),
        name='postman_write'),
    url(r'^messages/', include('postman.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.OPENSHIFT_GEAR_NAME is not None:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve',
            {'document_root': settings.STATIC_ROOT, 'insecure': True}),
        url(r'^media/(?P<path>.*)$', 'serve',
            {'document_root': settings.MEDIA_ROOT, 'insecure': True}),
    )
