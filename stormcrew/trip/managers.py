# -*- coding: utf-8 -*-
from django.db import models
from .queryset import TripQuerySet


class TripManager(models.Manager):
    def get_query_set(self):
        return TripQuerySet(self.model)
    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)
