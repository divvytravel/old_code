# -*- coding: utf-8 -*-
import logging
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.utils.dateformat import format

from model_utils import Choices
from utils.helpers import get_today
from .managers import TripManager, TripRequestManager


logger = logging.getLogger(__name__)


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
        return self.user_requests.active().filter(user=user).count() > 0

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

    def get_email_common_data(self, user_requested):
        return {
            'trip': self,
            'user_requested': user_requested,
            'domain': "http://" + str(get_current_site(None)),
        }, settings.EMAIL_HOST_USER

    def notify_email(self, user, subject, template_base_name, email_to, context={}):
        base_context, from_email = self.get_email_common_data(user)
        base_context.update(context)
        context = base_context
        template_html = "emails/{0}.html".format(template_base_name)
        template_txt = "emails/{0}.txt".format(template_base_name)
        text_content = render_to_string(template_html, context)
        html_content = render_to_string(template_txt, context)
        self.send_email_alternative(
            subject, text_content, html_content, from_email, email_to)

    def notify_owner_about_request(self, user_requested):
        if self.owner.email:
            self.notify_email(
                user_requested,
                u"Новая заявка на вашу поездку",
                "new_trip_request",
                [self.owner.email],
            )

    def notify_members_about_request(self, user_requested):
        members = self.people.exclude(email__isnull=True, email__exact='')
        for member in members:
            context = {"member": member}
            self.notify_email(
                user_requested,
                u"Новая заявка на поездку, в которой вы принимаете участие",
                "new_trip_member_request",
                [member.email],
                context
            )

    def notify_owner_about_cancel_request(self, user_requested):
        if self.owner.email:
            if self.is_open() or self.is_user_in(user_requested):
                subject = u"Отмена участия в поездке"
                user_was_in = True
            else:
                subject = u"Отмена заявки на вашу поездку"
                user_was_in = False
            context = {'user_was_in': user_was_in}
            self.notify_email(
                user_requested,
                subject,
                "cancel_trip_request",
                [self.owner.email],
                context
            )

    def notify_members_about_cancel_request(self, user_requested):
        # TODO
        pass

    def notify_members_about_delete(self, user_requested):
        if self.owner.email:
            if self.is_open() or self.is_user_in(user_requested):
                subject = u"Отмена участия в поездке"
                user_was_in = True
            else:
                subject = u"Отмена заявки на вашу поездку"
                user_was_in = False
            context = {'user_was_in': user_was_in}
            self.notify_email(
                user_requested,
                subject,
                "cancel_trip_request",
                [self.owner.email],
                context
            )

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

    STATUS = Choices(
        ('pending', u'Ожидает одобрения'),
        ('approved', u'Одобрена'),
        ('cancelled', u'Отменена'),
        ('denied', u'Отклонена'),
    )

    trip = models.ForeignKey('trip.Trip', related_name='user_requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS,
        default=STATUS.pending)

    objects = TripRequestManager()

    def approve(self):
        self.trip.people.add(self.user)
        self.status = TripRequest.STATUS.approved
        return self.save()
        # TODO
        # 1. send notification to user
        # 2. post on fb wall
        # 3. mark this trip request as approved

    def deny(self):
        # TODO
        # 1. send notification to user
        self.status = TripRequest.STATUS.denied
        return self.save()

    def cancel(self):
        self.status = TripRequest.STATUS.cancelled
        return self.save()

    def is_approved(self):
        return self.status == TripRequest.STATUS.approved

    class Meta:
        ordering = '-date_created',
