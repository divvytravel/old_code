# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.core.urlresolvers import reverse

from model_utils import Choices
from social_auth.fields import JSONField
from utils.helpers import get_today
from trip.models import Trip, TripRequest
from .managers import UserManagerWithFilters


class User(AbstractUser):
    """
    Access to social auth data is done by `social_auth` field.
    """
    PROVIDERS = Choices(('facebook', 'Facebook'), )
    GENDERS = Choices(('male', u'мужской'), ('female', u'женский'))

    # TODO: create RelativeUrlField
    avatar_url = models.CharField(default=settings.NO_AVATAR_IMG, max_length=200)
    provider = models.CharField(choices=PROVIDERS, max_length=20, blank=True)
    birthday = models.DateField(u"Дата рождения", blank=True, null=True)
    gender = models.CharField(u"Пол", choices=GENDERS, max_length=7, blank=True, null=True)
    social_auth_response = JSONField(blank=True, null=True)

    objects = UserManagerWithFilters()

    @property
    def get_avatar_url(self):
        avatar_url = self.avatar_url
        if self.provider == User.PROVIDERS.facebook:
            # also avaliable ?width=100&height=100
            # also avaliable ?type=large
            avatar_url += "?type=large"
        return avatar_url

    @property
    def get_avatar(self):
        avatar_url = self.get_avatar_url
        return mark_safe('<img class="avatar" src="{0}"/>'.format(avatar_url))

    def get_full_name(self, *args, **kwargs):
        full_name = super(User, self).get_full_name(*args, **kwargs)
        if not full_name:
            full_name = self.username
        return full_name

    def get_absolute_url(self):
        return reverse('users:detail', args=[str(self.pk)])

    def get_age(self):
        if self.birthday:
            today = get_today()
            born = self.birthday
            try:
                birthday = born.replace(year=today.year)
            except ValueError: # raised when birth date is February 29 and the current year is not a leap year
                birthday = born.replace(year=today.year, day=born.day-1)
            if birthday > today:
                return today.year - born.year - 1
            else:
                return today.year - born.year

    def get_social_link(self):
        if self.social_auth_response:
            link = self.social_auth_response.get('link', None)
            if link:
                return mark_safe(u'<a href="{0}">{1}</a>'.format(link, u'профиль'))

    def trips_in(self):
        return Trip.objects.with_people(self).count_gender()

    def trips_created(self):
        return Trip.objects.filter(owner=self).count_gender()

    def trip_requests_to_owner(self):
        return TripRequest.objects.select_related_trips().active().with_owner(self)

    def trip_requests_to_member(self):
        return TripRequest.objects.select_related_trips().active().with_member(self)

    def trip_requests(self):
        return TripRequest.objects.select_related_trips().active().filter(
        Q(trip__owner=self) | Q(trip__people=self)).distinct()

    def __unicode__(self):
        return self.get_full_name()
