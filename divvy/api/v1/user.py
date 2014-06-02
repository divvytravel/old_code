__author__ = 'indieman'

from django.conf.urls import url

from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource, Resource
from tastypie.utils import trailing_slash
from tastypie import fields

from provider.oauth2.models import AccessToken, Client, RefreshToken

import social_auth

# from .geo_resource import CityResource
from .base import BaseResourceMixin, AnonymousPostBaseResourceMixin

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from trip.models import Trip
from geo.models import City


class Row(object):
    pass


class dict2obj(object):
    """
    Convert dictionary to object
    """

    def __init__(self, d):
        self.__dict__['d'] = d

    def __getattr__(self, key):
        return self.__dict__['d'][key]


class UserResource(ModelResource, BaseResourceMixin):

    city = fields.ToOneField('api.v1.geo_resource.CityResource',
                             attribute='city',
                             related_name='users',
                             full=True, null=True)
    trips = fields.ToManyField('api.v1.trip_resource.TripResource',
                               attribute='approved_trips',
                               related_name='people',
                               full=False, null=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = User.objects.all()
        allowed_methods = ['get']
        fields = ['avatar_url', 'date_joined',
                  'birthday', 'first_name',
                  'gender', 'id', 'last_name',
                  'username', 'city', 'career']

        filtering = {
            'trips': ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        bundle.data['age'] = bundle.obj.get_age()
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        if 'access_token' in bundle.data:
            # Connect with social account
            social_auth_backend = social_auth.backends.get_backend(
                bundle.data['provider'], bundle.request, '')
            bundle.obj = social_auth_backend.do_auth(
                access_token=bundle.data['access_token'])

            for key, value in kwargs.items():
                setattr(bundle.obj, key, value)

            bundle = self.full_hydrate(bundle)

            bundle.obj.username = bundle.data.get('email', bundle.obj.email)
            bundle.is_active = True

        bundle.obj.save()
        return bundle

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/me%s$' % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_me'), name='api_user_get_me'),
        ]

    def get_me(self, request, **kwargs):
        self.method_check(request, allowed=['get', 'patch'])
        self.is_authenticated(request)
        self.throttle_check(request)

        kwargs['pk'] = request.user.pk
        return self.dispatch_detail(request, **kwargs)

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(UserResource, self).build_filters(filters)

        if "trip_country" in filters:
            trips = Trip.objects.filter(
                city__country__name=filters['trip_country'])
            # for trip in trips:
            #     print trip.id 
            orm_filters["approved_trips__in"] = [i.pk for i in trips]

        return orm_filters


class OAuthResource(AnonymousPostBaseResourceMixin, Resource):
    oauth_consumer_key = fields.CharField(attribute='oauth_consumer_key')

    class Meta(AnonymousPostBaseResourceMixin.Meta):
        resource_name = 'oauth'
        object_class = Row
        include_resource_uri = False
        include_absolute_url = False


class RegistrationResource(OAuthResource):
    class Meta(OAuthResource.Meta):
        resource_name = 'registration'
        allowed_methods = ['post', ]

    def detail_uri_kwargs(self, bundle_or_obj):
        """
        The following methods will need overriding regardless of your
        data source.
        """
        return {}

    def obj_create(self, bundle, request=None, **kwargs):
        user_resource = UserResource()
        user_bundle = user_resource.build_bundle(
            data=bundle.data.copy(),
            request=bundle.request)
        user_bundle = user_resource.obj_create(user_bundle, **kwargs)

        client = Client(user=user_bundle.obj, name="divvy_client",
                        client_type=1, url="http://divvy.com")
        client.save()
        scope = 2

        try:
            # Attempt to fetch an existing access token.
            access_token = AccessToken.objects.get(user=user_bundle.obj,
                                                   client=client, scope=scope)
        except AccessToken.DoesNotExist:
            # None found... make a new one!
            access_token = AccessToken.objects.create(user=user_bundle.obj,
                                                      scope=scope,
                                                      client=client)
            RefreshToken.objects.create(user=user_bundle.obj,
                                        access_token=access_token,
                                        client=client)

        bundle.obj = dict2obj({'oauth_consumer_key': access_token})
        bundle.data = {}
        return bundle
