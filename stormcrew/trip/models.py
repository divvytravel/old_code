# -*- coding: utf-8 -*-
import logging
import calendar
from datetime import datetime
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMultiAlternatives

from model_utils import Choices
from utils.decorators import self_if_blank_arg
from utils.helpers import date_yearsago
from django.db.models import Count

logger = logging.getLogger(__name__)

class TripQuerySet(QuerySet):
    def actual(self):
        return self.filter(start_date__gte=datetime.now().date())\
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
        return self.filter(people__in=users)

    @self_if_blank_arg
    def with_people_gender(self, gender):
        return self.filter(people__gender__in=[gender, ])

    @self_if_blank_arg
    def with_age(self, age_from, age_to):
        qs = self
        if age_from:
            b_to = date_yearsago(age_from)
            qs = qs.filter(people__birthday__lte=b_to)
        if age_to:
            b_from = date_yearsago(age_to)
            qs = qs.filter(people__birthday__gte=b_from)
        return qs


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
    country = models.ForeignKey('geo.Country', verbose_name=u'Страна',
        blank=True, null=True)
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
    people = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name='approved_trips', blank=True)

    objects = TripManager()

    def get_absolute_url(self):
        return reverse('trip_request_detail', args=[str(self.pk)])

    # TODO cache at instance level, but with user
    def is_user_in(self, user, skip_cache=False):
        if not user.is_authenticated():
            return False
        return self.people.filter(pk=user.pk).count() > 0

    # TODO cache at instance level, but with user
    def is_user_has_request(self, user, skip_cache=False):
        if not user.is_authenticated():
            return False
        return self.user_requests.filter(user=user).count() > 0

    def is_open(self):
        return self.trip_type == self.TRIP_TYPE.open

    def is_invite(self):
        return self.trip_type == self.TRIP_TYPE.invite

    def is_closed(self):
        return self.trip_type == self.TRIP_TYPE.closed

    def notify_owner_about_request(self, user_requested):
        if self.owner.email:
            context = {
                'trip': self,
                'user_requested': user_requested,
                'domain': "http://" + str(get_current_site(None)),
            }
            subject = u"Новая заявка на вашу поездку"
            from_email = settings.EMAIL_HOST_USER
            to = [self.owner.email]
            text_content = render_to_string('emails/new_trip_request.txt', context)
            html_content = render_to_string('emails/new_trip_request.html', context)
            self.send_email_alternative(
                subject, text_content, html_content, from_email, to)

    def notify_users_about_request(self, user_requested):
        if self.owner.email:
            context = {
                'trip': self,
                'user_requested': user_requested,
                'domain': "http://" + str(get_current_site(None)),
            }
            subject = u"Новая заявка на вашу поездку"
            from_email = settings.EMAIL_HOST_USER
            to = [self.owner.email]
            text_content = render_to_string('emails/new_trip_request.txt', context)
            html_content = render_to_string('emails/new_trip_request.html', context)
            self.send_email_alternative(
                subject, text_content, html_content, from_email, to)

    def notify_members_about_request(self, user_requested):
        member_emails = self.people.all().values_list('email', flat=True)
        if member_emails:
            context = {
                'trip': self,
                'user_requested': user_requested,
                'domain': "http://" + str(get_current_site(None)),
            }
            subject = u"Новая заявка на поездку, в которой вы принимаете участие"
            from_email = settings.EMAIL_HOST_USER
            to = member_emails
            text_content = render_to_string('emails/new_trip_member_request.txt', context)
            html_content = render_to_string('emails/new_trip_member_request.html', context)
            self.send_email_alternative(
                subject, text_content, html_content, from_email, to)

    def send_email_alternative(self, subject, text, html, from_email, to):
        try:
            msg = EmailMultiAlternatives(subject, text, from_email, to)
            msg.attach_alternative(html, "text/html")
            msg.send()
        except:
            logger.exception("send_mail failed.")

    def __unicode__(self):
        return u"{0}, [{1} - {2}]".format(self.title, self.start_date, self.end_date)


class TripPicture(models.Model):
    file = models.ImageField(upload_to="trip")
    trip = models.ForeignKey('trip.Trip', related_name='images')

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
