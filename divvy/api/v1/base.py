__author__ = 'indieman'

from django.forms import ModelChoiceField
from tastypie.validation import FormValidation

from tastypie.authentication import Authentication, BasicAuthentication, \
    MultiAuthentication, SessionAuthentication
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
            return super(AnonymousPostAuthentication, self).is_authenticated(
                request, **kwargs)


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


class AnonymousPostAuthentication(BasicAuthentication):
    def is_authenticated(self, request, **kwargs):

        if request.method == "POST":
            return True
        else:
            return super(AnonymousPostAuthentication, self).is_authenticated(
                request, **kwargs)


class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        try:
            self.upload_handler(request)
        except:
            pass

        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            request.META['CONTENT_TYPE'] = 'application/json'
            return data

        return super(MultipartResource, self).deserialize(
            request, data, format)

    def put_detail(self, request, **kwargs):
        if request.META.get('CONTENT_TYPE').startswith('multipart') and \
                not hasattr(request, '_body'):
            request._body = ''

        return super(MultipartResource, self).put_detail(request, **kwargs)


class ModelFormValidation(FormValidation):
    """
    Override tastypie's standard ``FormValidation`` since this does not care
    about URI to PK conversion for ``ToOneField`` or ``ToManyField``.
    """

    def uri_to_pk(self, uri):
        """
        Returns the integer PK part of a URI.

        Assumes ``/api/v1/resource/123/`` format. If conversion fails, this just
        returns the URI unmodified.

        Also handles lists of URIs
        """

        if uri is None:
            return None
        # convert everything to lists
        multiple = not isinstance(uri, basestring)
        uris = uri if multiple else [uri]

        # handle all passed URIs
        converted = []
        for one_uri in uris:
            try:
                # hopefully /api/v1/<resource_name>/<pk>/
                converted.append(int(one_uri.split('/')[-2]))
            except (IndexError, ValueError):
                raise ValueError(
                    "URI %s could not be converted to PK integer." % one_uri)

        # convert back to original format
        return converted if multiple else converted[0]

    def is_valid(self, bundle, request=None):
        data = bundle.data
        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}
            # copy data, so we don't modify the bundle
        data = data.copy()

        # convert URIs to PK integers for all relation fields
        relation_fields = [name for name, field in
                           self.form_class.base_fields.items()
                           if issubclass(field.__class__, ModelChoiceField)]

        for field in relation_fields:
            if field in data:
                data[field] = self.uri_to_pk(data[field])

        # validate and return messages on error
        form = self.form_class(data=data, files=request.FILES)
        if form.is_valid():
            return {}
        return form.errors


class BaseResourceMixin(object):
    class Meta:
        # authentication = MultiAuthentication(
        #     SessionAuthentication(),
        #     BasicAuthentication())
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True


# class AnonymousPostBaseResourceMixin(BaseResourceMixin):
#     class Meta(BaseResourceMixin.Meta):
#         authentication = AnonymousPostAuthentication()
#         authorization = Authorization()
#         always_return_data = True
