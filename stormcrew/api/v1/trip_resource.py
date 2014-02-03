__author__ = 'indieman'

from tastypie.resources import ModelResource
from tastypie import fields

from .base import BaseResourceMixin

from trip.models import Trip, TripCategory, Tags, Images
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


class TripCategoryResource(ModelResource, BaseResourceMixin):
    tag = fields.ToOneField(TagsResource, attribute='tag',
                            related_name='trip_category', full=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = TripCategory.objects.all()
        allowed_methods = ['get']


class TripResource(ModelResource, BaseResourceMixin):
    people = fields.ManyToManyField(UserResource, attribute='people', full=True, null=True)
    category = fields.ToOneField(TripCategoryResource, attribute='category',
                                 related_name='trips', full=True, null=True)
    tags = fields.ManyToManyField(TagsResource, attribute='tags',
                                  related_name='trips', full=True, null=True)
    images = fields.ManyToManyField(ImageResource, attribute='images', full=True, null=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = Trip.objects.all()
        allowed_methods = ['get']
        filtering = {
            'price_type': ('exact', ),
            'people_count': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'price': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'start_date': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'category': ('exact', ),
            'tags': ('exact', 'range')
        }

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(TripResource, self).build_filters(filters)

        if "country" in filters:
            cities = City.objects.filter(country__name=filters['country'])

            orm_filters["city__in"] = [i.pk for i in cities]

        return orm_filters

    def dehydrate(self, bundle):
        bundle.data['country'] = u'%s' % bundle.obj.city.country
        bundle.data['country_id'] = bundle.obj.city.country_id
        return bundle