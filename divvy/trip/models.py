# -*- coding: utf-8 -*-
import logging
import uuid

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.dateformat import format
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes import generic

from sorl.thumbnail import get_thumbnail
from markupfield.fields import MarkupField

from model_utils import Choices
from utils.helpers import get_today
from utils.email import send_common_email
from .managers import TripManager, TripRequestManager


logger = logging.getLogger(__name__)
DEFAUTL_CURRENCY = Choices(
    ('euro', u"евро"), ('rub', u"руб."), ('dollar', u"доллар"))


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "trip/%s.%s" % (uuid.uuid4(), ext)
    return filename


class Images(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=get_file_path, max_length=255)


class Image(models.Model):
    image = models.ImageField(upload_to=get_file_path, max_length=255)


class Tags(models.Model):
    name = models.CharField(_(u"Тег"), max_length=20)
    slug = models.SlugField(u"Вид в url", unique=True)
    main_page = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.name


class TripCategory(models.Model):
    APPLICABLE = Choices(
        ('all', u"все"),
        ('noncom', u"некоммерческая"),
        ('comm', u"коммерческая"),
    )
    title = models.CharField(_(u"Название"), max_length=100)
    applicable = models.CharField(u"применимость", max_length=10,
                                  choices=APPLICABLE, default=APPLICABLE.all)
    slug = models.SlugField(u"Вид в url", unique=True)
    tag = models.ForeignKey(Tags, related_name="trip_category")
    keywords = models.ManyToManyField(Tags)

    class Meta:
        verbose_name = u"Категория"
        verbose_name_plural = u"Категории"

    def __unicode__(self):
        return self.title

    def get_point_types(self):
        return self.point_types.all()


class Trip(models.Model):
    CURRENCY = DEFAUTL_CURRENCY
    TRIP_TYPE = Choices(
        ('open', _(u'Участие открытое')),
        ('invite', _(u'Участие после одобрения создателя поездки')),
        ('closed', _(u'Участие после одобрения всех участников поездки')),
    )

    PRICE_TYPE = Choices(
        ('noncom', _(u'Некоммерческая поездка')),
        ('comm', _(u'Коммерческая поездка')),
    )

    title = models.CharField(u"Название", max_length=200)
    # category = models.ForeignKey(TripCategory, blank=True, null=True,
    #                              related_name="trips", verbose_name=u'Категория')
    categories = models.ManyToManyField(
        TripCategory, blank=True, null=True,
        related_name='trips', verbose_name=u'Категории')
    start_date = models.DateField(u"Дата начала")
    end_date = models.DateField(u"Дата окончания")
    end_people_date = models.DateField(_(u"Дата окончания набора группы"))
    price = models.PositiveIntegerField(u"Бюджет",
                                        help_text=u"примерный бюджет",
                                        blank=True, null=True)
    city = models.ForeignKey('geo.City', verbose_name=u'Город',
                             help_text=u"если несколько, то первый",
                             related_name='trips')

    currency = models.CharField(u"Валюта", max_length=10, choices=CURRENCY,
                                default=CURRENCY.euro)
    includes = models.CharField(u"Что входит", max_length=200)
    people_count = models.PositiveIntegerField(
        u"Минимальное количество человек")
    people_max_count = models.PositiveIntegerField(
        u"Максимальное количество человек")
    descr_main = MarkupField(u"Опишите суть поездки")
    descr_share = models.TextField(
        u"Опишите, что вы хотите разделить (или зачем вам компания)",
        blank=True)
    descr_additional = models.TextField(
        u"Укажите дополнительную информацию (авиаперелет и т.п.)", blank=True)
    descr_company = models.TextField(
        u"Требования к компании (кого вы хотели бы видеть в качестве соседей)",
        blank=True)
    descr_include = models.TextField(
        u"В стоимость входят",
        blank=True)
    trip_type = models.CharField(u"Участие", max_length=10, choices=TRIP_TYPE,
                                 default=TRIP_TYPE.open)
    price_type = models.CharField(
        _(u"Тип поездки"), max_length=10, choices=PRICE_TYPE,
        default=PRICE_TYPE.noncom)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=u'Создатель')
    people = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='approved_trips',
                                    blank=True, verbose_name=u'Участники')
    tags = models.ManyToManyField(
        Tags, related_name='trips', blank=True, verbose_name=u'Теги')

    # image = models.ImageField(upload_to=get_file_path, blank=True, null=True, max_length=255)
    image = models.ForeignKey(
        'trip.Image', related_name='trip_images', blank=True, null=True)
    gallery = models.ManyToManyField(
        'trip.Image', related_name='trip_galleries', blank=True, null=True)
    # images = generic.GenericRelation('trip.Images', object_id_field='object_id', content_type_field='content_type')

    sex = models.FloatField(blank=True, null=True, default=None)
    age = models.SmallIntegerField(blank=True, null=True, default=None)
    recommended = models.BooleanField(default=False)

    images = generic.GenericRelation(Images)

    objects = TripManager()

    class Meta:
        ordering = 'start_date',
        verbose_name = u"Поездка"
        verbose_name_plural = u"Поездки"

    def __unicode__(self):
        return u"{0}, [{1} - {2}]".format(
            self.title, self.start_date, self.end_date)

    def get_include_list(self):
        if self.descr_include.strip():
            include_list = self.descr_include.split(u'\n')
        else:
            include_list = None
        return include_list

    def get_main_image_url(self):
        try:
            img_file = self.images.all()[0].image
            im = get_thumbnail(img_file, '360x360', crop='center', quality=100)
            return im.url
        except IndexError:
            return None

    def get_sex(self):
        females = 0
        people = self.people.all()
        if people:
            for p in people:
                if 'female' == p.gender:
                    females += 1

            return str(float(females) * 100 / len(people)).replace(',', '.')
        else:
            return None

    def get_female_ratio(self):
        females = 0
        people = self.people.all()
        if people:
            for p in people:
                if 'female' == p.gender:
                    females += 1

            return str(float(females) * 100 / len(people)).replace(',', '.')
        else:
            return 0

    def get_male_ratio(self):
        males = 0
        people = self.people.all()
        if people:
            for p in people:
                if 'female' != p.gender:
                    males += 1

            return str(float(males) * 100 / len(people)).replace(',', '.')
        else:
            return 0

    def get_peoples_ratio(self):
        people = self.people.all()
        if people and self.people_count:
            if len(people) > self.people_count:
                return 100
            else:
                return str((len(people) * 100) / float(self.people_count)).replace(',', '.')
        else:
            return 0

    def get_sex_status(self):
        females = 0
        people = self.people.all()
        if people:
            for p in people:
                if 'female' == p.gender:
                    females += 1

            sex_float = (float(females) * 100) / len(people)
        else:
            sex_float = None

        status = ''
        if sex_float is None:
            status = ''
        elif sex_float >= 90:
            status = u'только женщины'
        elif 70 <= sex_float < 90:
            status = u'преимущественно женщины'
        elif 40 <= sex_float < 70:
            status = u'поровну'
        elif 10 <= sex_float < 40:
            status = u'преимущественно мужчины'
        elif sex_float <= 10:
            status = u'только мужчины'
        return status

    def format_date(self, date):
        return format(date, "j E")

    def start_date_format(self):
        return self.format_date(self.start_date)

    def end_date_format(self):
        return self.format_date(self.end_date)

    def end_people_date_format(self):
        return self.format_date(self.end_people_date)

    def invite_days_left(self):
        today = get_today()
        if today >= self.end_people_date:
            return 0
        else:
            return (self.end_people_date - today).days

    def count_members(self):
        cnt_members = getattr(self, 'count_all_people', None)
        if cnt_members is None:
            cnt_members = self.people.count()
        return cnt_members

    def count_free_slots(self):
        return self.people_max_count - self.count_members()

    def price_for_one_person(self):
        if self.is_noncom:
            if self.count_members():
                return self.price / self.count_members()
            else:
                return self.price
        else:
            return self.price

    @staticmethod
    def points_updated(sender, instance, **kwargs):
        try:
            trip = instance.trip
        except Trip.DoesNotExist:
            trip = None
        if not trip is None:
            price = 0
            currency = u""
            for count, point in enumerate(trip.points.all()):
                price += point.price
                if count == 0:
                    currency = point.currency
            trip.price = price
            trip.currency = currency
            trip.save()

    def get_absolute_url(self):
        return reverse('trip_detail', args=[str(self.pk)])

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

    def is_recruit_finished(self, today=None):
        today = today or get_today()
        return self.end_people_date < today

    def is_finished(self, today=None):
        today = today or get_today()
        return self.end_date < today

    def is_now(self, today=None):
        today = today or get_today()
        return self.start_date <= today <= self.end_date

    def is_future(self, today=None):
        today = today or get_today()
        return self.start_date > today

    @property
    def is_comm(self):
        return self.price_type == self.PRICE_TYPE.comm

    @property
    def is_noncom(self):
        return not self.is_comm

    def show_price_type(self):
        if self.is_comm:
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


class TripPointType(models.Model):
    title = models.CharField(u'Название', max_length=100)
    point_title_name = models.CharField(
        u'Название поля для заглавия',
        max_length=100,
        help_text=u"Например, 'Модель' для яхты, 'ФИО' для шкипера")
    many = models.BooleanField(u'Несколько', default=False)
    category = models.ForeignKey(TripCategory, verbose_name=u'Категория',
                                 related_name='point_types')

    class Meta:
        verbose_name = u"Тип поля поездки"
        verbose_name_plural = u"Типы полей поездки"

    def __unicode__(self):
        return u"{0} ({1})".format(self.title, self.category)

    def get_title(self):
        return self.title.capitalize()

    def get_form_prefix(self):
        return "{0}{1}".format(self.__class__.__name__.lower(), self.pk)

    def get_form_css_class(self):
        return "css_{0}".format(self.get_form_prefix())


class TripPoint(models.Model):
    CURRENCY = DEFAUTL_CURRENCY

    p_type = models.ForeignKey(
        TripPointType, verbose_name=u'Тип', null=True, blank=True)
    title = models.CharField(
        u"Заглавие", max_length=50,
        help_text=u"Фактическое название поля берется из выбранного типа")
    description = models.TextField(u"Описание")
    price = models.PositiveIntegerField(u"Цена", blank=True, null=True)
    currency = models.CharField(u"Валюта", max_length=10, choices=CURRENCY,
                                blank=True, null=True)
    link = models.URLField(u"Ссылка", blank=True, null=True)
    trip = models.ForeignKey(
        Trip, verbose_name=u'Поездка', related_name='points', blank=True, null=True)

    class Meta:
        verbose_name = u"Поле поездки"
        verbose_name_plural = u"Поля поездки"

    def __unicode__(self):
        return u"{0}, {1}, {2}".format(
            self.p_type, self.trip, self.description[:15])


post_save.connect(Trip.points_updated, sender=TripPoint)
post_delete.connect(Trip.points_updated, sender=TripPoint)


class TripRequest(models.Model):
    STATUS = Choices(
        ('pending', u'Ожидает одобрения'),
        ('approved', u'Одобрена'),
        ('cancelled', u'Отменена'),
        ('denied', u'Отклонена'),
    )

    trip = models.ForeignKey('trip.Trip', related_name='user_requests',
                             verbose_name=u'Поездка')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=u'Пользователь')
    date_created = models.DateTimeField(u"Дата создания", default=timezone.now)
    status = models.CharField(u"Статус", max_length=10, choices=STATUS,
                              default=STATUS.pending)
    users_approved = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='approved_trip_requests', blank=True, null=True,
        verbose_name=u'Одобрена пользователями')
    approved_by_owner = models.BooleanField(u"Одобрена создателем",
                                            default=False)
    denied_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True, null=True, related_name='denied_trip_requests',
        verbose_name=u'Отклонена пользователями')

    objects = TripRequestManager()

    allow_post_fb = models.BooleanField(verbose_name=u'Разрешен постинг на стену Facebook')

    def __unicode__(self):
        return u"{0}, {1}".format(self.trip, self.user)

    class Meta:
        verbose_name = u"Запрос в поездку"
        verbose_name_plural = u"Запросы в поездку"
        ordering = '-date_created',
        unique_together = ("trip", "user")

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
            if self.users_approved.count() == self.trip.people.count() \
                and self.approved_by_owner:
                approved = True

        if approved:
            self.trip.people.add(self.user)
            self.status = TripRequest.STATUS.approved
            self.save()
            self.user.notify_about_approve(self.trip)
            if self.allow_post_fb:
                self.user.post_approve_on_fb_wall(self.trip)
            self.trip.update_search_fields()

        return approved

    def deny(self, by_user):
        # TODO
        # 1. send notification to user
        self.status = TripRequest.STATUS.denied
        self.denied_by.add(by_user)
        return self.save()

    def cancel(self):
        try:
            self.status = TripRequest.STATUS.cancelled
            self.save()
            return {"success": True}
        except:
            return {"success": False, "error": u""}

    def is_approved(self):
        return self.status == TripRequest.STATUS.approved

    def is_approved_by(self, user):
        return self.users_approved.filter(pk=user.pk).count() > 0 \
            or (self.trip.owner == user and self.approved_by_owner)
