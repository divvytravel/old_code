# -*- coding: utf-8 -*-
import calendar
from datetime import datetime
from django.db.models.query import QuerySet
from django.db.models import Q
from django.db.models import Count
from utils.helpers import wrap_in_iterable, get_today
from utils.decorators import self_if_blank_arg
from users.queryset import filter_user_age, filter_user_gender


class TripQuerySet(QuerySet):
    def actual(self):
        return self.filter(start_date__gt=get_today())\
            .order_by('start_date')

    def passed(self):
        return self.filter(end_date__lt=get_today())\
            .order_by('start_date')

    def count_gender(self):
        return self.annotate(count_all_people=Count('people'))\
        .extra(select = {
            "count_female" : """
            SELECT COUNT(*)
            FROM "users_user"
                LEFT OUTER JOIN "trip_trip_people" ON ("users_user"."id" = "trip_trip_people"."user_id" and "trip_trip_people"."trip_id" = "trip_trip"."id")
            WHERE "users_user"."gender" = 'female' and "trip_trip"."id" = "trip_trip_people"."trip_id"
            """
        }).extra(select = {
            "count_male" : """
            SELECT COUNT(*)
            FROM "users_user"
                LEFT OUTER JOIN "trip_trip_people" ON ("users_user"."id" = "trip_trip_people"."user_id" and "trip_trip_people"."trip_id" = "trip_trip"."id")
            WHERE "users_user"."gender" = 'male' and "trip_trip"."id" = "trip_trip_people"."trip_id"
            """
        }).distinct()

    @self_if_blank_arg
    def in_month_year(self, month_year):
        month, year = map(int, month_year.split('.'))
        d_fmt = "{0:>02}.{1:>02}.{2}"
        start_date = datetime.strptime(
            d_fmt.format(1, month, year), '%d.%m.%Y').date()
        l_day = calendar.monthrange(year, month)[1]
        end_date = datetime.strptime(
            d_fmt.format(l_day, month, year), '%d.%m.%Y').date()
        return self.filter(
            Q(start_date__gte=start_date, start_date__lte=end_date)
             |
            Q(start_date__lt=start_date, end_date__gte=start_date))

    @self_if_blank_arg
    def in_country(self, country):
        return self.filter(country=country)

    @self_if_blank_arg
    def with_people(self, users):
        return self.filter(people__in=wrap_in_iterable(users))

    @self_if_blank_arg
    def with_people_gender(self, gender):
        return filter_user_gender(self, gender, prefix='people')

    @self_if_blank_arg
    def with_people_age(self, age_from, age_to):
        return filter_user_age(self, age_from, age_to, prefix='people')


class TripRequestQuerySet(QuerySet):
    def active(self):
        from .models import TripRequest
        return self.filter(trip__start_date__gt=get_today(),
            status=TripRequest.STATUS.pending)

    def select_related_trips(self):
        return self.select_related('trip')

    def with_owner(self, owner):
        return self.filter(trip__owner=owner)

    def with_member(self, member):
        return self.filter(trip__people=member)

