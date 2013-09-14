# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from model_utils import Choices
from django.db.models.query import QuerySet


class TripQuerySet(QuerySet):
    def actual(self):
        return self.filter(start_date__gte=datetime.now().date())


class TripManager(models.Manager):
    def get_query_set(self):
        return TripQuerySet(self.model)
    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)


class Trip(models.Model):
    CURRENCY = Choices(('euro', u"евро"), ('rub', u"руб."), ('dollar', u"доллар"))
    TRIP_TYPE = Choices(
        ('open', u'Участие открытое'),
        ('invite', u'Участие после одобрения создателя поездки'),
        ('closed', u'Участие после одобрения всех участников поездки'),
    )

    start_date = models.DateField()
    end_date = models.DateField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, choices=CURRENCY, default=CURRENCY.euro)
    includes = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    people_count = models.PositiveIntegerField()
    descr_main = models.TextField()
    descr_share = models.TextField(blank=True)
    descr_additional = models.TextField(blank=True)
    descr_company = models.TextField(blank=True)
    trip_type = models.CharField(max_length=10, choices=TRIP_TYPE, default=TRIP_TYPE.open)
    owner = models.ForeignKey('users.User')

    objects = TripManager()


class TripPicture(models.Model):
    file = models.ImageField(upload_to="trip")
    trip = models.ForeignKey('trip.Trip')

    def __unicode__(self):
        return self.file.name

    # remove to leave file.
    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(TripPicture, self).delete(*args, **kwargs)
