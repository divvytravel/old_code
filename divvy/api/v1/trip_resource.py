# -*- coding: utf-8 -*-
__author__ = 'indieman'

from tastypie.resources import ModelResource
from tastypie import fields

from .base import BaseResourceMixin

from trip.models import Trip, TripCategory, Tags, Images, TripPoint, \
    TripPointType
from geo.models import Country, City

from .user_resource import UserResource


class ImageResource(ModelResource, BaseResourceMixin):
    class Meta(BaseResourceMixin.Meta):
        queryset = Images.objects.all()
        allowed_methods = ['get']


class TagsResource(ModelResource, BaseResourceMixin):
    class Meta(BaseResourceMixin.Meta):
        queryset = Tags.objects.all()
        allowed_methods = ['get']

        filtering = {
            'main_page': ('exact', ),
        }


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
    people = fields.ManyToManyField(UserResource, attribute='people', full=True, null=True)
    categories = fields.ManyToManyField(TripCategoryResource, attribute='categories',
                                        related_name='trips', full=True, null=True)
    tags = fields.ManyToManyField(TagsResource, attribute='tags',
                                  related_name='trips', full=True, null=True)
    images = fields.ManyToManyField(ImageResource, attribute='images', full=True, null=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = Trip.objects.prefetch_related('people').all()
        allowed_methods = ['get']
        filtering = {
            'price_type': ('exact', ),
            'people_count': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'price': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'start_date': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'category': ('exact', ),
            'tags': ('exact', 'range'),
            'sex': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'age': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
        }

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(TripResource, self).build_filters(filters)

        if "country" in filters:
            cities = City.objects.filter(country__name=filters['country'])

            orm_filters["city__in"] = [i.pk for i in cities]

        # if "sex" in filters:

        return orm_filters

    def apply_filters(self, request, applicable_filters):
        qs = None
        if not qs:
            qs = super(TripResource, self).apply_filters(request, applicable_filters)

        return qs

    def dehydrate(self, bundle):
        bundle.data['country'] = u'%s' % bundle.obj.city.country
        bundle.data['country_id'] = bundle.obj.city.country_id

        bundle.data['city'] = u'%s' % bundle.obj.city.name
        bundle.data['city_id'] = bundle.obj.city_id

        if bundle.obj.sex is None:
            bundle.data['consist'] = None
        elif 40 < bundle.obj.sex and bundle.data.sex < 60:
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


class TripPointResource(ModelResource, BaseResourceMixin):
    p_type = fields.ToOneField(TripPointTypeResource, attribute='p_type',
                               full=True, null=True)
    trip = fields.ToOneField(TripResource, attribute='trip',
                             related_name='points', full=True, null=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = TripPoint.objects.all()
        allowed_methods = ['get']