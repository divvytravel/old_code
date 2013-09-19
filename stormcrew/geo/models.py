# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.query import QuerySet


class CountryQuerySet(QuerySet):
    pass


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

    def get_or_create_normalized(self, name):
        if not name:
            return None
        name = CountryManager.normailize_name(name)
        country = None
        try:
            country = self.model.objects.get(name=name)
        except self.model.DoesNotExist:
            country = self.model(name=name)
            country.save(using=self._db)
        return country


class Country(models.Model):
    name = models.CharField(u"Название", max_length=100, unique=True)

    objects = CountryManager()

    def __unicode__(self):
        return self.name
