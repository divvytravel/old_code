__author__ = 'indieman'

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization


class BaseResourceMixin(object):
    """
    A class designed to provide a basic model resource implementation across the API.

    Example:
    class MyResource(ModelResource, BaseResourceMixin):
        class Meta(BaseResourceMixin.Meta):
            ...

    or

    class MyResource(ModelResource):
        class Meta(BaseResourceMixin.Meta):
            ...
    """
    class Meta:
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        # cache = SimpleCache()

        # def to_simple(self, obj):
        #     bundle = self.build_bundle(obj=obj)
        #     bundle = self.full_dehydrate(bundle)
        #
        #     return self._meta.serializer.to_simple(bundle.data, None)


class AnonymousPostAuthentication(BasicAuthentication):
    """ No auth on post / for user creation """

    def is_authenticated(self, request, **kwargs):
        """ If POST, don't check auth, otherwise fall back to parent """

        if request.method == "POST":
            return True
        else:
            return super(AnonymousPostAuthentication, self).is_authenticated(request, **kwargs)


class AnonymousPostBaseResourceMixin(BaseResourceMixin):
    """
    A class designed to provide a basic model resource implementation across the API.

    Example:
    class MyResource(ModelResource, AnonymousPostBaseResourceMixin):
        class Meta(AnonymousPostBaseResourceMixin.Meta):
            ...

    or

    class MyResource(ModelResource):
        class Meta(AnonymousPostBaseResourceMixin.Meta):
            ...list_
    """
    class Meta(BaseResourceMixin.Meta):
        authentication = AnonymousPostAuthentication()
        authorization = Authorization()
        always_return_data = True