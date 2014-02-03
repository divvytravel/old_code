__author__ = 'indieman'

from tastypie.api import Api

from api.v1.trip_resource import TripResource, UserResource


v1_api = Api(api_name='v1')
v1_api.register(TripResource())
v1_api.register(UserResource())
urlpatterns = v1_api.urls