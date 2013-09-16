# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.conf import settings

from users import views

urlpatterns = patterns('',
    # URL pattern for the UserListView
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {"next_page": settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(
        regex=r'^list/$',
        view=views.UserListView.as_view(),
        name='list'
    ),
    # URL pattern for the UserRedirectView
    url(
        regex=r'^redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    # URL pattern for the UserDetailView
    url(
        regex=r'^profile/$',
        view=views.UserUpdateView.as_view(),
        name='profile'
    ),
    # URL pattern for the UserDetailView
    url(
        regex=r'^(?P<pk>\d+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
)
