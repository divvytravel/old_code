__author__ = 'indieman'

from tastypie.authentication import Authentication
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
