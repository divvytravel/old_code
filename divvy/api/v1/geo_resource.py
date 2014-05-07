__author__ = 'indieman'

from tastypie import fields

from api.v1.base import BaseResourceMixin, ModelFormValidation
from tastypie.resources import ModelResource
from tastypie.constants import ALL_WITH_RELATIONS

from geo.models import Country, City
from geo.forms import CityForm


class CityResource(ModelResource, BaseResourceMixin):
    trips = fields.OneToManyField('api.v1.trip_resource.TripResource', attribute='trips',
                                  full=False, null=True, blank=True)
    country = fields.ToOneField('api.v1.geo_resource.CountryResource', attribute='country',
                                full=True, blank=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = City.objects.all()
        allowed_methods = ['get', 'post']
        validation = ModelFormValidation(form_class=CityForm)

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

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(CountryResource, self).build_filters(filters)

        if "trip_start_date_gte" in filters:
            cities = City.objects.filter(trips__start_date__gte=filters['trip_start_date_gte']).distinct()

            orm_filters["cities__in"] = [i.pk for i in cities]

        return orm_filters

    def apply_filters(self, request, applicable_filters):
        qs = self.get_object_list(request).filter(**applicable_filters)

        distinct = request.GET.get('distinct', False) == 'True'
        if distinct:
            qs = qs.distinct()

        return qs
