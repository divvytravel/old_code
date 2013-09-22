# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.conf import settings

from users import views

urlpatterns = patterns('',
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {"next_page": settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(regex=r'^cabinet/$', view=views.UserUpdateView.as_view(),
        name='cabinet'),
    url(regex=r'^(?P<pk>\d+)/$', view=views.UserDetailView.as_view(),
        name='detail'),
)
