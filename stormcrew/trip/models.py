# -*- coding: utf-8 -*-
from django.db import models
from model_utils import Choices


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
    descr_share = models.TextField()
    descr_additional = models.TextField()
    descr_company = models.TextField()
    trip_type = models.CharField(max_length=10, choices=TRIP_TYPE, default=TRIP_TYPE.open)
