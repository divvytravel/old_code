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

    start_date = models.DateField(u"Дата начала")
    end_date = models.DateField(u"Дата окончания")
    country = models.CharField(u"Страна", max_length=100)
    city = models.CharField(u"Город", max_length=100)
    price = models.PositiveIntegerField(u"Бюджет")
    currency = models.CharField(u"Валюта", max_length=10, choices=CURRENCY, default=CURRENCY.euro)
    includes = models.CharField(u"Что входит", max_length=200)
    title = models.CharField(u"Название", max_length=200)
    people_count = models.PositiveIntegerField(u"Сколько нужно человек")
    descr_main = models.TextField(u"Опишите суть поездки")
    descr_share = models.TextField(u"Опишите, что вы хотите разделить (или зачем вам компания)", blank=True)
    descr_additional = models.TextField(u"Укажите дополнительную информацию (авиаперелет и т.п.)", blank=True)
    descr_company = models.TextField(u"Требования к компании (кого вы хотели бы видеть в качестве соседей)", blank=True)
    trip_type = models.CharField(u"Тип поездки", max_length=10, choices=TRIP_TYPE, default=TRIP_TYPE.open)
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
