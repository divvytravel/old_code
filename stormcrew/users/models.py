# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db.models.query import QuerySet

from model_utils import Choices
from social_auth.fields import JSONField


class UserQuerySet(QuerySet):
    def ready_to_trip(self):
        return self.exclude(provider="")


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
    provider = models.CharField(choices=PROVIDERS, max_length=20, blank=True, null=True)
    birthday = models.DateField(u"Дата рождения", blank=True, null=True)
    gender = models.CharField(u"Пол", choices=GENDERS, max_length=7, blank=True, null=True)
    social_auth_response = JSONField(blank=True, null=True)

    objects = UserManagerWithFilters()

    @property
    def get_avatar(self):
        avatar_url = self.avatar_url
        if self.provider == User.PROVIDERS.facebook:
            # also avaliable ?width=100&height=100
            # also avaliable ?type=large
            avatar_url += "?type=large"
            # avatar_url += "?width=180&height=180"
        return mark_safe('<img class="avatar" src="{0}"/>'.format(avatar_url))

    def __unicode__(self):
        return self.username
