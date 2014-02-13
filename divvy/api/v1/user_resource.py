__author__ = 'indieman'

from django.conf.urls import url

from tastypie.resources import ModelResource, Resource
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.utils import trailing_slash
from tastypie import fields, http

from provider.oauth2.models import AccessToken, Client, RefreshToken

import social_auth
# from social_auth.db.django_models import UserSocialAuth

from .base import BaseResourceMixin, AnonymousPostBaseResourceMixin

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()


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


# class SocialResource(ModelResource, BaseResourceMixin):
#     user = fields.ForeignKey('api.v1.user_resource.UserResource', attribute='user')
#     access_token = fields.CharField(attribute='access_token', null=True, blank=True)
#
#     class Meta(BaseResourceMixin.Meta):
#         queryset = UserSocialAuth.objects.all()
#         resource_name = 'socialauth'
#         fields = ['provider', 'uid', ]
#         include_resource_uri = True
#         include_absolute_uri = False
#         allowed_methods = ['get', 'post', 'patch', 'delete']
#
#     def get_object_list(self, request):
#         return super(SocialResource, self).get_object_list(request).filter(user=request.user)
#
#     def obj_create(self, bundle, request=None, **kwargs):
#         try:
#             social_auth_backend = social_auth.backends.get_backend(bundle.data['provider'], bundle.request, '')
#
#             user = social_auth_backend.do_auth(access_token=bundle.data['access_token'], user=bundle.request.user)
#             bundle.obj = user.social_user
#
#         except:
#             raise ImmediateHttpResponse(response=http.HttpBadRequest('Social account is already use.'))
#         return bundle
#
#     def hydrate_user(self, bundle):
#         bundle.data['user'] = {'pk': bundle.request.user.pk}
#         return bundle
#
#     def dehydrate_access_token(self, bundle):
#         return bundle.obj.extra_data['access_token']


class UserResource(ModelResource, BaseResourceMixin):
    # socials = fields.ToManyField(SocialResource, attribute="social_auth", null=True,
    #                              blank=True, full=True,
    #                              use_in=lambda bundle: hasattr(bundle.request, "user") and \
    #                                                    bundle.request.user.is_authenticated() and \
    #                                                    bundle.obj.id == bundle.request.user.id)

    class Meta(BaseResourceMixin.Meta):
        queryset = User.objects.all()
        allowed_methods = ['get']
        fields = ['avatar_url', 'date_joined',
                  'birthday', 'first_name',
                  'gender', 'id', 'last_name',
                  'username', 'city', 'career']

    def obj_create(self, bundle, request=None, **kwargs):
        if 'access_token' in bundle.data:
            # Connect with social account
            social_auth_backend = social_auth.backends.get_backend(bundle.data['provider'], bundle.request, '')
            bundle.obj = social_auth_backend.do_auth(access_token=bundle.data['access_token'])

            for key, value in kwargs.items():
                setattr(bundle.obj, key, value)

            bundle = self.full_hydrate(bundle)

            bundle.obj.username = bundle.data.get('email', bundle.obj.email)
            bundle.is_active = True

        bundle.obj.save()
        return bundle

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/me%s$' % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_me'), name='api_user_get_me'),
        ]

    def get_me(self, request, **kwargs):
        self.method_check(request, allowed=['get', 'patch'])
        self.is_authenticated(request)
        self.throttle_check(request)

        kwargs['pk'] = request.user.pk
        return self.dispatch_detail(request, **kwargs)


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
        user_bundle = user_resource.build_bundle(data=bundle.data.copy(), request=bundle.request)
        user_bundle = user_resource.obj_create(user_bundle, **kwargs)

        client = Client(user=user_bundle.obj, name="divvy_client", client_type=1, url="http://divvy.com")
        client.save()
        scope = 2

        try:
            # Attempt to fetch an existing access token.
            access_token = AccessToken.objects.get(user=user_bundle.obj, client=client, scope=scope)
        except AccessToken.DoesNotExist:
            # None found... make a new one!
            access_token = AccessToken.objects.create(user=user_bundle.obj, scope=scope, client=client)
            RefreshToken.objects.create(user=user_bundle.obj, access_token=access_token, client=client)

        bundle.obj = dict2obj({'oauth_consumer_key': access_token})
        bundle.data = {}
        return bundle
