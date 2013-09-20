# -*- coding: utf-8 -*-
from datetime import timedelta
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse

from model_utils import Choices
from social_auth.fields import JSONField
from utils.decorators import self_if_blank_arg
from utils.helpers import date_yearsago


def filter_user_age(qs, age_from, age_to, prefix=None):
    if age_from:
        b_to = date_yearsago(age_from+1) + timedelta(days=1)
        if prefix:
            kwargs = {'{0}__birthday__lte'.format(prefix): b_to}
        else:
            kwargs = {'birthday__lte': b_to}
        qs = qs.filter(**kwargs)
    if age_to:
        b_from = date_yearsago(age_to+1) + timedelta(days=1)
        if prefix:
            kwargs = {'{0}__birthday__gte'.format(prefix): b_from}
        else:
            kwargs = {'birthday__gte': b_from}
        qs = qs.filter(**kwargs)
    return qs


def filter_user_gender(qs, gender, prefix=None):
    if prefix:
        kwargs = {"{0}__gender__in".format(prefix): [gender, ]}
    else:
        kwargs = {"gender__in": [gender, ]}
    return qs.filter(**kwargs)


class UserQuerySet(QuerySet):
    def ready_to_trip(self):
        # TODO: on production remove isnull
        return self.exclude(provider="").exclude(provider__isnull=True)

    def in_trips(self, trips):
        return self.filter(approved_trips__in=trips).distinct()

    @self_if_blank_arg
    def with_age(self, age_from, age_to):
        return filter_user_age(self, age_from, age_to)

    @self_if_blank_arg
    def with_gender(self, gender):
        return filter_user_gender(self, gender)


class UserManagerWithFilters(UserManager):
    def get_query_set(self):
        return UserQuerySet(self.model)
    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)


class User(AbstractUser):
    """
    Access to social auth data is done by `social_auth` field.
    """
    PROVIDERS = Choices('facebook', )
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

    def __unicode__(self):
        return self.get_full_name()
