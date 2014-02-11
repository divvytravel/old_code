# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from geo import views

urlpatterns = patterns('',
    url(regex=r'^cheapestflight/$', view=views.CheapestFlightView.as_view(),
        name='cheapestflight'),
)
