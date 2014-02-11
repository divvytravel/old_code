__author__ = 'indieman'

from tastypie.api import Api

from api.v1.trip_resource import TripResource
from api.v1.user_resource import UserResource, RegistrationResource


v1_api = Api(api_name='v1')
v1_api.register(TripResource())
v1_api.register(UserResource())
v1_api.register(RegistrationResource())
urlpatterns = v1_api.urls