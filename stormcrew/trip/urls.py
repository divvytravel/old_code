# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import TripCreateView, TripRequestFormView, TripUpdateView

urlpatterns = patterns('',
    url(r'^create/$', TripCreateView.as_view(), name='trip_create'),
    url(r'^detail/(?P<pk>\d+)/$', TripRequestFormView.as_view(),
        name='trip_request_detail'),
    url(r'^update/(?P<pk>\d+)/$', TripUpdateView.as_view(),
        name='trip_update'),
)
