# -*- coding: utf-8 -*-
import logging
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.dateformat import format
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from utils.helpers import get_today
from utils.email import send_common_email
from .managers import TripManager, TripRequestManager


logger = logging.getLogger(__name__)


class TripCategory(models.Model):
    title = models.CharField(_(u"Название"), max_length=100)


class Trip(models.Model):
    CURRENCY = Choices(('euro', u"евро"), ('rub', u"руб."), ('dollar', u"доллар"))
    TRIP_TYPE = Choices(
        ('open', _(u'Участие открытое')),
        ('invite', _(u'Участие после одобрения создателя поездки')),
        ('closed', _(u'Участие после одобрения всех участников поездки')),
    )

    PRICE_TYPE = Choices(
        ('noncom', _(u'некоммерческая')),
        ('comm', _(u'коммерческая')),
    )

    title = models.CharField(u"Название", max_length=200)
    category = models.ForeignKey(TripCategory, blank=True, null=True)
    start_date = models.DateField(u"Дата начала")
    end_date = models.DateField(u"Дата окончания")
    end_people_date = models.DateField(_(u"Дата окончания набора группы"))
    country = models.ForeignKey('geo.Country', verbose_name=u'Страна',
        blank=True, null=True)
    city = models.CharField(u"Город", max_length=100,
        help_text=u"если несколько, то первый")
    price = models.PositiveIntegerField(u"Бюджет",
        help_text=u"примерный бюджет")
    currency = models.CharField(u"Валюта", max_length=10, choices=CURRENCY, default=CURRENCY.euro)
    includes = models.CharField(u"Что входит", max_length=200)
    people_count = models.PositiveIntegerField(u"Минимальное количество человек")
    people_max_count = models.PositiveIntegerField(u"Максимальное количество человек")
    descr_main = models.TextField(u"Опишите суть поездки")
    descr_share = models.TextField(u"Опишите, что вы хотите разделить (или зачем вам компания)", blank=True)
    descr_additional = models.TextField(u"Укажите дополнительную информацию (авиаперелет и т.п.)", blank=True)
    descr_company = models.TextField(u"Требования к компании (кого вы хотели бы видеть в качестве соседей)", blank=True)
    trip_type = models.CharField(u"Тип поездки", max_length=10, choices=TRIP_TYPE, default=TRIP_TYPE.open)
    price_type = models.CharField(_(u"Коммеречкая"), max_length=10, choices=PRICE_TYPE, default=PRICE_TYPE.noncom)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    people = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name='approved_trips', blank=True)

    objects = TripManager()

    class Meta:
        ordering = 'start_date',

    def __unicode__(self):
        return u"{0}, [{1} - {2}]".format(self.title, self.start_date, self.end_date)

    def format_date(self, date):
        return format(date, "j E")

    def start_date_format(self):
        return self.format_date(self.start_date)

    def end_date_format(self):
        return self.format_date(self.end_date)

    def end_people_date_format(self):
        return self.format_date(self.end_people_date)

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

    def show_price_type(self):
        if self.price_type == self.PRICE_TYPE.comm:
            return u"$"
        else:
            return u"o"

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

    def get_emailable_members(self):
        return self.people.exclude(email__isnull=True, email__exact='')

    def notify_owner_about_request(self, user_requested):
        if self.owner.email:
            send_common_email(
                user=user_requested,
                trip=self,
                subject=u"Новая заявка на вашу поездку",
                template_base_name="new_trip_request",
                email_to=[self.owner.email],
            )

    def notify_members_about_request(self, user_requested):
        for member in self.get_emailable_members():
            context = {"member": member}
            send_common_email(
                user=user_requested,
                trip=self,
                subject=u"Новая заявка на поездку, в которой вы принимаете участие",
                template_base_name="new_trip_member_request",
                email_to=[member.email],
                context=context
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
            send_common_email(
                user=user_requested,
                trip=self,
                subject=subject,
                template_base_name="cancel_trip_request",
                email_to=[self.owner.email],
                context=context
            )

    def notify_members_about_cancel_request(self, user_requested):
        for member in self.get_emailable_members():
            context = {"member": member}
            send_common_email(
                user=user_requested,
                trip=self,
                subject=u"Изменение состава поездки",
                template_base_name="cancel_trip_request_member",
                email_to=[member.email],
                context=context
            )

    def notify_members_about_delete(self, user_requested):
        if self.owner.email:
            if self.is_open() or self.is_user_in(user_requested):
                subject = u"Отмена участия в поездке"
                user_was_in = True
            else:
                subject = u"Отмена заявки на вашу поездку"
                user_was_in = False
            context = {'user_was_in': user_was_in}
            send_common_email(
                user=user_requested,
                trip=self,
                subject=subject,
                template_base_name="cancel_trip_request",
                email_to=[self.owner.email],
                context=context
            )


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
    users_approved = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name='approved_trip_requests', blank=True, null=True)
    approved_by_owner = models.BooleanField(default=False)
    denied_by = models.ManyToManyField(settings.AUTH_USER_MODEL,
        blank=True, null=True, related_name='denied_trip_requests')

    objects = TripRequestManager()

    def approve(self, by_user):
        approved = False
        if self.trip.is_invite() and by_user == self.trip.owner:
            self.approved_by_owner = True
            approved = True
        elif self.trip.is_closed():
            if by_user == self.trip.owner:
                self.approved_by_owner = True
                self.save()
            member = self.trip.people.filter(pk=by_user.pk)
            if len(member) > 0:
                member = member[0]
                self.users_approved.add(by_user)
            if self.users_approved.count() == self.trip.people.count()\
                    and self.approved_by_owner:
                approved = True

        if approved:
            self.trip.people.add(self.user)
            self.status = TripRequest.STATUS.approved
            self.save()
            self.user.notify_about_approve(self.trip)
            self.user.post_approve_on_fb_wall(self.trip)

        return approved

    def deny(self, by_user):
        # TODO
        # 1. send notification to user
        self.status = TripRequest.STATUS.denied
        self.denied_by.add(by_user)
        return self.save()

    def cancel(self):
        self.status = TripRequest.STATUS.cancelled
        return self.save()

    def is_approved(self):
        return self.status == TripRequest.STATUS.approved

    def is_approved_by(self, user):
        return self.users_approved.filter(pk=user.pk).count() > 0\
            or (self.trip.owner == user and self.approved_by_owner)

    class Meta:
        ordering = '-date_created',
