from django.db import models
from .queryset import CountryQuerySet, CityQuerySet, AirportIATAQuerySet


class CountryManager(models.Manager):
    def get_query_set(self):
        return CountryQuerySet(self.model)

    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)

    @classmethod
    def normailize_name(cls, name):
        return name.title()

    def get_normalized_or_none(self, name):
        if not name:
            return None
        name = CountryManager.normailize_name(name)
        country = None
        try:
            country = self.model.objects.get(name=name)
        except self.model.DoesNotExist:
            pass
        return country

    def get_or_create_normalized(self, name):
        if not name:
            return None
        country = self.get_normalized_or_none(name)
        if country is None:
            country = self.model(name=name)
            country.save(using=self._db)
        return country


class CityManager(models.Manager):
    def get_query_set(self):
        return CityQuerySet(self.model)

    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)


class AirportIATAManager(models.Manager):
    def get_query_set(self):
        return AirportIATAQuerySet(self.model)

    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)
