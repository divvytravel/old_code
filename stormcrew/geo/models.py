# -*- coding: utf-8 -*-
from django.db import models
from .managers import CountryManager


class Country(models.Model):
    name = models.CharField(u"Название", max_length=100, unique=True)

    objects = CountryManager()

    def __unicode__(self):
        return self.name
