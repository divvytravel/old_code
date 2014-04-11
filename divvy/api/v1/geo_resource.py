__author__ = 'indieman'

from tastypie import fields

from api.v1.base import BaseResourceMixin
from tastypie.resources import ModelResource
from tastypie.constants import ALL_WITH_RELATIONS

from geo.models import Country, City

from api.v1.trip_resource import TripResource


class CityResource(ModelResource, BaseResourceMixin):
    trips = fields.OneToManyField(TripResource, attribute='trips',
                                  full=False, null=True)
    country = fields.ToOneField('api.v1.geo_resource.CountryResource', attribute='country',
                                full=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = City.objects.all()
        allowed_methods = ['get']

        filtering = {
            'trips': ALL_WITH_RELATIONS,
        }


class CountryResource(ModelResource, BaseResourceMixin):
    cities = fields.OneToManyField(CityResource, attribute='cities', full=False)

    class Meta(BaseResourceMixin.Meta):
        queryset = Country.objects.all()
        allowed_methods = ['get']

        filtering = {
            'cities': ALL_WITH_RELATIONS,
        }