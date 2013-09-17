# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from milkman.dairy import milkman
from users.models import User
from tests.utils import random_date
from datetime import datetime, timedelta
import random

countries = (
    u'Россия',
    u'Испания',
    u'Франция',
    u'Германия',
    u'Англия',
)

cities = (
    u'Москва',
    u'Барселона',
    u'Париж',
    u'Берлин',
    u'Лондон',
)


class Command(BaseCommand):
    args = '<amount>'
    help = 'Fills existing database with test trips'

    def handle(self, *args, **options):
        amount = int(args[0])
        for i in range(amount):
            start_date = random_date(
                datetime.now()+timedelta(days=1),
                datetime.now()+timedelta(days=30))
            end_date = random_date(
                start_date,
                start_date+timedelta(days=30)
            )
            users = []
            for j in range(random.randint(2, 4)):
                user = User.objects.order_by('?')[0]
                if user not in users:
                    users.append(user)
            trip = milkman.deliver('trip.trip',
                start_date=start_date, end_date=end_date,
                country=random.choice(countries),
                city=random.choice(cities),
                title=u"Поездка_{0}".format(i),
                people=users,
                owner=User.objects.all()[0]
            )
            self.stdout.write("Created trip '{0}'".format(trip))

        self.stdout.write("Successfully created test trips")
