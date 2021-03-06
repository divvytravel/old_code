# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import create_nonprofit, detail, blog, blogpost, detail_commerce, trip_request, \
                   approve_request, deny_request

# from .views import TripCreateStepOneView, TripRequestFormView, TripUpdateView,\
#     TripDeleteView, TripRequestApproveView, TripCreateStepTwoView

urlpatterns = patterns('',
    url(r'^create/nonprofit/$', create_nonprofit, name='trip_create'),
    url(r'^(?P<pk>\d+)/$', detail, name='trip_detail'),
    url(r'^(?P<trip_pk>\d+)/request/(?P<user_pk>\d+)/$', trip_request, name='trip_request'),
    url(r'^(?P<trip_pk>\d+)/request/(?P<user_pk>\d+)/approve/$', approve_request, name='approve_request'),
    url(r'^(?P<trip_pk>\d+)/request/(?P<user_pk>\d+)/deny/$', deny_request, name='deny_request'),

    url(r'^blog/$', blog, name='blog'),
    url(r'^blogpost/$', blogpost, name='blogpost'),
    url(r'^detail/commerce/$', detail_commerce, name='trip_detail_commerce'),
    
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
