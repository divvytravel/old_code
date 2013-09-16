# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet

from model_utils import Choices
from utils.decorators import instance_cache


class TripQuerySet(QuerySet):
    def actual(self):
        return self.filter(start_date__gte=datetime.now().date())\
            .order_by('start_date')


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

    title = models.CharField(u"Название", max_length=200)
    start_date = models.DateField(u"Дата начала")
    end_date = models.DateField(u"Дата окончания")
    country = models.CharField(u"Страна", max_length=100)
    city = models.CharField(u"Город", max_length=100,
        help_text=u"если несколько, то первый")
    price = models.PositiveIntegerField(u"Бюджет",
        help_text=u"примерный бюджет")
    currency = models.CharField(u"Валюта", max_length=10, choices=CURRENCY, default=CURRENCY.euro)
    includes = models.CharField(u"Что входит", max_length=200)
    people_count = models.PositiveIntegerField(u"Сколько нужно человек")
    descr_main = models.TextField(u"Опишите суть поездки")
    descr_share = models.TextField(u"Опишите, что вы хотите разделить (или зачем вам компания)", blank=True)
    descr_additional = models.TextField(u"Укажите дополнительную информацию (авиаперелет и т.п.)", blank=True)
    descr_company = models.TextField(u"Требования к компании (кого вы хотели бы видеть в качестве соседей)", blank=True)
    trip_type = models.CharField(u"Тип поездки", max_length=10, choices=TRIP_TYPE, default=TRIP_TYPE.open)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    people = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='approved_trips', blank=True)

    objects = TripManager()

    def get_absolute_url(self):
        return reverse('trip_request_detail', args=[str(self.pk)])

    @instance_cache
    def is_user_in(self, user, skip_cache=False):
        return self.people.filter(pk=user.pk).count() > 0

    @instance_cache
    def is_user_has_request(self, user, skip_cache=False):
        return self.user_requests.filter(user=user).count() > 0

    def is_open(self):
        return self.trip_type == self.TRIP_TYPE.open

    def is_invite(self):
        return self.trip_type == self.TRIP_TYPE.invite

    def is_closed(self):
        return self.trip_type == self.TRIP_TYPE.closed

    def __unicode__(self):
        return u"{0}, [{1} - {2}]".format(self.title, self.start_date, self.end_date)


class TripPicture(models.Model):
    file = models.ImageField(upload_to="trip")
    trip = models.ForeignKey('trip.Trip')

    def __unicode__(self):
        return self.file.name

    # remove to leave file.
    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(TripPicture, self).delete(*args, **kwargs)


class TripRequest(models.Model):
    trip = models.ForeignKey('trip.Trip', related_name='user_requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(default=timezone.now)
