# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import TripFilterFormView

urlpatterns = patterns('',
    url(r'^$', TripFilterFormView.as_view(), name='home'),
)
