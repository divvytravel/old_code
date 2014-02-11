# -*- coding: utf-8 -*-
import logging
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.core.urlresolvers import reverse

from model_utils import Choices
from social_auth.fields import JSONField

from utils.helpers import get_today
from utils.email import send_common_email
from utils.social_fb import post_on_fb_wall
from utils.decorators import sort_trips_by_time_status
from trip.models import Trip, TripRequest
from .managers import UserManagerWithFilters
from .queryset import is_default_age_range


logger = logging.getLogger(__name__)


class User(AbstractUser):
    """
    Access to social auth data is done by `social_auth` field.
    """
    PROVIDERS = Choices(('facebook', 'Facebook'), )
    GENDERS = Choices(('male', u'мужской'), ('female', u'женский'))

    # TODO: create RelativeUrlField
    avatar_url = models.CharField(u"Url аватарки",
        default=settings.NO_AVATAR_IMG, max_length=200)
    provider = models.CharField(u"Источник", choices=PROVIDERS,
        max_length=20, blank=True)
    birthday = models.DateField(u"Дата рождения", blank=True, null=True)
    gender = models.CharField(u"Пол", choices=GENDERS, max_length=7, blank=True, null=True)
    social_auth_response = JSONField(u"Данные из источника", blank=True,
        null=True)

    objects = UserManagerWithFilters()

    def __unicode__(self):
        return self.get_full_name()

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

    def is_satisfy(self, gender, age_from, age_to):
        if self.gender and gender and self.gender != gender:
            return False
        age = self.get_age()
        if age and not is_default_age_range(age_from, age_to):
            if age_from and age_from > age:
                return False
            if age_to and age_to < age:
                return False
        return True

    @sort_trips_by_time_status
    def trips_in(self):
        return Trip.objects.with_people(self).count_gender()

    @sort_trips_by_time_status
    def trips_created(self):
        return Trip.objects.filter(owner=self).count_gender()

    def trip_requests_to_owner(self):
        return TripRequest.objects.include_related().active().with_owner(self)

    def trip_requests_to_member(self):
        return TripRequest.objects.include_related().active().with_member(self)

    def trip_requests(self):
        return TripRequest.objects.include_related().active().filter(
        Q(trip__owner=self) | Q(trip__people=self)).distinct()

    def outgoing_trip_requests(self):
        return TripRequest.objects.include_related().active().filter(user=self)

    def notify_about_approve(self, trip):
        if self.email:
            send_common_email(
                user=self,
                trip=trip,
                subject=u"Ваша заявка одобрена",
                template_base_name="trip_request_approved",
                email_to=[self.email],
            )

    def post_approve_on_fb_wall(self, trip):
        if self.provider == User.PROVIDERS.facebook:
            post_on_fb_wall(self, trip)
