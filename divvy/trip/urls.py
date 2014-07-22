# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import create_nonprofit, detail_nonprofit

# from .views import TripCreateStepOneView, TripRequestFormView, TripUpdateView,\
#     TripDeleteView, TripRequestApproveView, TripCreateStepTwoView

urlpatterns = patterns('',
    url(r'^create/nonprofit/$', create_nonprofit, name='trip_create'),
    url(r'^detail/nonprofit/(?P<pk>\d+)/$', detail_nonprofit, name='trip_detail'),
    # url(r'^create/(?P<price_type>[\w_-]+)/(?P<category_slug>[\w_-]+)/$',
        # TripCreateStepTwoView.as_view(), name="trip_create_step_two"),
    # url(r'^detail/(?P<pk>\d+)/$', TripRequestFormView.as_view(),
    #     name='trip_request_detail'),
    # url(r'^update/(?P<pk>\d+)/$', TripUpdateView.as_view(),
    #     name='trip_update'),
    # url(r'^delete/(?P<pk>\d+)/$', TripDeleteView.as_view(),
    #     name='trip_delete'),
    # url(r'^request/approve/$', TripRequestApproveView.as_view(),
    #     name='trip_request_approve'),
)
