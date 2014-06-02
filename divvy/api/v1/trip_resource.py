# -*- coding: utf-8 -*-
__author__ = 'indieman'

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS, ALL

from .base import BaseResourceMixin, MultipartResource, ModelFormValidation

from trip.models import Trip, TripCategory, Tags, Images, TripPoint, \
    TripPointType, Image
from trip.forms import TripForm

from geo.models import City

from .user import UserResource
from paginator import TripPaginator


class ImagesResource(ModelResource, BaseResourceMixin):
    class Meta(BaseResourceMixin.Meta):
        queryset = Images.objects.all()
        allowed_methods = ['get']


class ImageResource(BaseResourceMixin, MultipartResource, ModelResource):

    class Meta(BaseResourceMixin.Meta):
        queryset = Image.objects.all()
        allowed_methods = ['get', 'post']

        filtering = {
            'id': ALL
        }


class TagsResource(ModelResource, BaseResourceMixin):
    trips = fields.ManyToManyField('api.v1.trip_resource.TripResource', attribute='trips',
                                   related_name='tags', full=False, null=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = Tags.objects.all()
        allowed_methods = ['get']

        filtering = {
            'main_page': ('exact', ),
            # 'trips': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'trips': ALL_WITH_RELATIONS
        }

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(TagsResource, self).build_filters(filters)

        if "trip_country" in filters:
            trips = Trip.objects.filter(city__country__name=filters['trip_country']).distinct()

            orm_filters["trips__in"] = [i.pk for i in trips]

        return orm_filters

    def apply_filters(self, request, applicable_filters):
        qs = self.get_object_list(request).filter(**applicable_filters)

        distinct = request.GET.get('distinct', False) == 'True'
        if distinct:
            qs = qs.distinct()

        return qs


class TripCategoryResource(ModelResource, BaseResourceMixin):
    tag = fields.ToOneField(TagsResource, attribute='tag',
                            related_name='trip_category', full=True)
    keywords = fields.ManyToManyField(TagsResource, attribute='keywords',
                                      full=True, null=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = TripCategory.objects.all()
        allowed_methods = ['get']


class TripPointTypeResource(ModelResource, BaseResourceMixin):
    category = fields.ToOneField(TripCategoryResource, attribute='category',
                                 related_name='point_types',
                                 full=True, null=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = TripPointType.objects.all()
        allowed_methods = ['get']


class TripResource(ModelResource, BaseResourceMixin):
    people = fields.ManyToManyField(UserResource, attribute='people',
                                    full=True, null=True)

    categories = fields.ManyToManyField(TripCategoryResource,
                                        attribute='categories',
                                        full=True, null=True)

    tags = fields.ManyToManyField(TagsResource, attribute='tags',
                                  related_name='trips', full=True, null=True)

    gallery = fields.ManyToManyField(ImageResource, attribute='gallery',
                                     full=True, null=True)

    image = fields.ToOneField(ImageResource, attribute='image',
                              full=True, null=True)

    city = fields.ToOneField('api.v1.geo_resource.CityResource',
                             attribute='city', full=True, null=True,
                             blank=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = Trip.objects.prefetch_related('people').all()
        allowed_methods = ['get', 'post']

        filtering = {
            'price_type': ('exact', ),
            'people_count': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'price': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'start_date': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'categories': ('exact', ),
            'tags': ('exact', 'range'),
            'sex': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'age': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'people': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'city': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
        }

        paginator_class = TripPaginator
        validation = ModelFormValidation(form_class=TripForm)

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(TripResource, self).build_filters(filters)

        if "country" in filters:
            cities = City.objects.filter(country__name=filters['country'])

            orm_filters["city__in"] = [i.pk for i in cities]

        return orm_filters

    def apply_filters(self, request, applicable_filters):
        qs = None
        if not qs:
            qs = super(TripResource, self).apply_filters(
                request,
                applicable_filters)

        return qs

    def dehydrate(self, bundle):

        if bundle.obj.sex is None:
            bundle.data['consist'] = None
        elif 40 < bundle.obj.sex < 60:
            bundle.data['consist'] = u'поровну'
        elif bundle.obj.sex > 70:
            bundle.data['consist'] = u'преимущественно женщины'
        elif bundle.obj.sex < 30:
            bundle.data['consist'] = u'преимущественно мужчины'
        elif bundle.obj.sex > 90:
            bundle.data['consist'] = u'только женщины'
        elif bundle.obj.sex < 10:
            bundle.data['consist'] = u'только мужчины'
        return bundle


class DateResource(TripResource):
    people = fields.ManyToManyField(UserResource, attribute='people',
                                    full=False, null=True)
    categories = fields.ManyToManyField(TripCategoryResource,
                                        attribute='categories',
                                        related_name='trips',
                                        full=False, null=True)
    tags = fields.ManyToManyField(TagsResource, attribute='tags',
                                  related_name='trips', full=False, null=True)
    images = fields.ManyToManyField(ImageResource, attribute='images',
                                    full=False, null=True)

    city = fields.ToOneField('api.v1.geo_resource.CityResource',
                             attribute='city',
                             full=False, null=True)

    class Meta(TripResource.Meta):
        excludes = ['id', 'currency', 'descr_additional', 'descr_company'
                    'descr_main', 'descr_share', 'image', 'images',
                    'includes', 'price_type', 'recommended', 'title'
                    ]

    def dehydrate(self, bundle):
        return bundle


class TripPointResource(ModelResource, BaseResourceMixin):
    p_type = fields.ToOneField(TripPointTypeResource, attribute='p_type',
                               full=True, null=True)
    trip = fields.ToOneField(TripResource, attribute='trip',
                             related_name='points', full=True, null=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = TripPoint.objects.all()
        allowed_methods = ['get']