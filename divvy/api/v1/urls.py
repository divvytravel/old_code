__author__ = 'indieman'

from tastypie.api import Api

from api.v1.geo_resource import CityResource, CountryResource
from api.v1.trip_resource import TripResource, TagsResource
from api.v1.user_resource import UserResource, RegistrationResource
from api.v1.blog_resource import BlogCategoryResource, PostResource


v1_api = Api(api_name='v1')
v1_api.register(TripResource())
v1_api.register(UserResource())
v1_api.register(RegistrationResource())
v1_api.register(BlogCategoryResource())
v1_api.register(PostResource())
v1_api.register(TagsResource())
v1_api.register(CityResource())
v1_api.register(CountryResource())
urlpatterns = v1_api.urls