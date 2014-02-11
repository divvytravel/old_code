# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from geo.models import Country, City


cities = (
    (u"Испания", u'Барселона'),
    (u"Испания", u'Мадрид'),
    (u"Италия", u'Рим'),
    (u"Италия", u'Венеция'),
    (u"Италия", u'Флоренция'),
    (u"Греция", u'Афины'),
    (u"Бразилия", u'Рио-де-Жанейро'),
    (u"Франция", u'Париж'),
)


class Command(BaseCommand):
    args = None
    help = 'Fills existing database with test trips'

    def handle(self, *args, **options):
        country_set = set()
        cnt_city, cnt_country = 0, 0
        for country_name, city_name in cities:
            if country_name not in country_set:
                country_set.add(country_name)
                country, created = Country.objects.get_or_create(name=country_name)
                self.stdout.write(u"Created country '{0}'".format(country_name))
                cnt_country += 1
            City.objects.get_or_create(name=city_name, country=country)
            cnt_city += 1
            self.stdout.write(u"Created city '{0}'".format(city_name))

        self.stdout.write("Successfully created {0} cities and {1} countries".format(
            cnt_city, cnt_country))
