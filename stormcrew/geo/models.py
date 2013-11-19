# -*- coding: utf-8 -*-
from django.db import models
from .managers import CountryManager, CityManager


class Country(models.Model):
    name = models.CharField(u"Название", max_length=100, unique=True)

    class Meta:
        verbose_name = u"Страна"
        verbose_name_plural = u"Страны"

    objects = CountryManager()

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(u"Название", max_length=100, db_index=True)
    country = models.ForeignKey(Country, verbose_name=u'Страна')

    objects = CityManager()

    class Meta:
        verbose_name = u"Город"
        verbose_name_plural = u"Города"
        unique_together = "name", "country"
        ordering = "country__name", "name"

    def __unicode__(self):
        return u"{0}, {1}".format(self.country, self.name)
