# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import TripCreateView

urlpatterns = patterns('',
    url(r'^create/$', TripCreateView.as_view(), name='trip_create'),
)
