# -*- coding: utf-8 -*-
from datetime import timedelta
from django.db.models.query import QuerySet
from django.db.models import Q
from utils.helpers import date_yearsago
from utils.decorators import self_if_blank_arg
from utils.helpers import get_today


def is_default_age_range(age_from, age_to):
    from trip.forms import TripFilterForm
    age_choices = TripFilterForm.AGES
    if age_from == age_choices[0][0] and age_to == age_choices[-1][0]:
        return True
    else:
        return False


def filter_user_age(qs, age_from, age_to, prefix=None):
    if is_default_age_range(age_from, age_to):
        return qs
    if age_from:
        b_to = date_yearsago(age_from+1) + timedelta(days=1)
        if prefix:
            kwargs = {'{0}__birthday__lte'.format(prefix): b_to}
        else:
            kwargs = {'birthday__lte': b_to}
        q_from = Q(**kwargs)
    else:
        q_from = Q()
    if age_to:
        b_from = date_yearsago(age_to+1) + timedelta(days=1)
        if prefix:
            kwargs = {'{0}__birthday__gte'.format(prefix): b_from}
        else:
            kwargs = {'birthday__gte': b_from}
        q_to = Q(**kwargs)
    else:
        q_to = Q()
    return qs.filter(q_from & q_to)


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

    def have_trip(self):
        return self.filter(approved_trips__start_date__gt=get_today()).distinct()

    def in_trips(self, trips):
        return self.filter(approved_trips__in=trips).distinct()

    @self_if_blank_arg
    def with_age(self, age_from, age_to):
        return filter_user_age(self, age_from, age_to)

    @self_if_blank_arg
    def with_gender(self, gender):
        return filter_user_gender(self, gender)

    def admins(self):
        return self.filter(is_superuser=True)

    def as_list(self, field_name):
        return self.values_list(field_name, flat=True)
