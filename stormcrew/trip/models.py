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
from django.utils.dateformat import format

from model_utils import Choices
from utils.decorators import self_if_blank_arg
from utils.helpers import wrap_in_iterable, get_today
from users.models import filter_user_age, filter_user_gender
from django.db.models import Count

logger = logging.getLogger(__name__)


class TripQuerySet(QuerySet):
    def actual(self):
        return self.filter(start_date__gte=get_today())\
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

    class Meta:
        ordering = 'start_date',

    def format_date(self, date):
        return format(date, "j E")

    def start_date_format(self):
        return self.format_date(self.start_date)

    def end_date_format(self):
        return self.format_date(self.end_date)

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

    def is_finished(self, today=None):
        today = today or get_today()
        return self.end_date < today

    def is_now(self, today=None):
        today = today or get_today()
        return self.start_date <= today <= self.end_date

    def is_future(self, today=None):
        today = today or get_today()
        return self.start_date > today

    def get_status(self):
        if not self.start_date:
            None
        today = get_today()
        if self.is_future(today):
            return u"будущая"
        elif self.is_finished(today):
            return u"завершенная"
        else:
            return u"текущая"


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

    def get_email_common_data(self, user_requested):
        return {
            'trip': self,
            'user_requested': user_requested,
            'domain': "http://" + str(get_current_site(None)),
        }, settings.EMAIL_HOST_USER

    def notify_users_about_request(self, user_requested):
        if self.owner.email:
            context, from_email = self.get_email_common_data(user_requested)
            subject = u"Новая заявка на вашу поездку"
            to = [self.owner.email]
            text_content = render_to_string('emails/new_trip_request.txt', context)
            html_content = render_to_string('emails/new_trip_request.html', context)
            self.send_email_alternative(
                subject, text_content, html_content, from_email, to)

    def notify_members_about_request(self, user_requested):
        member_emails = self.people.all().values_list('email', flat=True)
        if member_emails:
            context, from_email = self.get_email_common_data(user_requested)
            subject = u"Новая заявка на поездку, в которой вы принимаете участие"
            to = member_emails
            text_content = render_to_string('emails/new_trip_member_request.txt', context)
            html_content = render_to_string('emails/new_trip_member_request.html', context)
            self.send_email_alternative(
                subject, text_content, html_content, from_email, to)

    def notify_owner_about_cancel_request(self, user_requested):
        if self.owner.email:
            context, from_email = self.get_email_common_data(user_requested)
            to = [self.owner.email]
            if self.is_open() or self.is_user_in(user_requested):
                subject = u"Отмена участия в поездке"
                user_was_in = True
            else:
                subject = u"Отмена заявки на вашу поездку"
                user_was_in = False
            context.update({'user_was_in': user_was_in})
            text_content = render_to_string('emails/cancel_trip_request.txt', context)
            html_content = render_to_string('emails/cancel_trip_request.html', context)
            self.send_email_alternative(
                subject, text_content, html_content, from_email, to)

    def notify_members_about_cancel_request(self, user_requested):
        pass

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
