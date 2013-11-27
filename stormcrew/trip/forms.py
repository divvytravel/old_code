# -*- coding: utf-8 -*-
import logging
import itertools
from datetime import datetime
from django import forms
from .models import Trip, TripRequest, TripCategory, TripPoint
from users.models import User
from geo.models import Country, City
from utils.helpers import get_today

l = logging.getLogger(__name__)


def get_trip_form_fields(before_formsets=False, after_formsets=False):
    all_fields = [
        'title',
        'start_date',
        'end_date',
        'end_people_date',
        'city',
        'price',
        'currency',
        'includes',
        'people_count',
        'people_max_count',
        'descr_main',
        'descr_share',
        'descr_additional',
        'descr_company',
        'trip_type',
    ]
    if before_formsets:
        before_fields = []
        for f in all_fields:
            if f == "descr_share":
                break
            before_fields.append(f)
        return before_fields

    if after_formsets:
        after_fields = []
        started = False
        for f in all_fields:
            started = started or f == "descr_share"
            if started:
                after_fields.append(f)
        return after_fields
    return all_fields


class TripCreateStepOne(forms.Form):
    price_type = forms.ChoiceField(label=u"Тип поездки",
        choices=Trip.PRICE_TYPE._choices)
    category = forms.ModelChoiceField(label=u"Категория",
        queryset=TripCategory.objects.all(),
        empty_label=None)

    form_errors = {
        "unapplicable": u"Выбранные тип и категория несовместимы",
    }

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data', {})
        category_slug = data.get('category_slug', None)
        #TODO: this approach will touch DB twice, here and during
        # internal clean_category method. Look for django forms
        # clean chain.
        if category_slug:
            try:
                data['category'] = TripCategory.objects.get(
                    slug=category_slug).pk
            except TripCategory.DoesNotExist:
                pass
        if isinstance(data.get('category', None), TripCategory):
            data['category'] = kwargs['data']['category'].pk
        super(TripCreateStepOne, self).__init__(*args, **kwargs)

    def is_comm(self, obj):
        if isinstance(obj, TripCategory):
            return obj.applicable == obj.APPLICABLE.comm
        else:
            return obj == Trip.PRICE_TYPE.comm

    def is_noncom(self, obj):
        if isinstance(obj, TripCategory):
            return obj.applicable == obj.APPLICABLE.noncom
        else:
            return obj == Trip.PRICE_TYPE.noncom

    def clean(self):
        price_type = self.cleaned_data['price_type']
        category = self.cleaned_data['category']
        if self.is_comm(category) and self.is_noncom(price_type)\
          or self.is_noncom(category) and self.is_comm(price_type):
            raise forms.ValidationError(self.form_errors['unapplicable'])
        return self.cleaned_data


class TripForm(forms.ModelForm):
    trip_errors = {
        'end_less_start_date': u"Конечная дата не может быть меньше начальной",
        'low_date': u"Дата не может быть меньше сегодняшней",
        'people_max_count': u"Минимальное количество человек не может быть больше максимального",
        'end_people_date': u"Дата окончания набора группы не может быть позже начала поездки",
    }

    author_in = forms.BooleanField(label=u"Я участвую в этой поездке",
        initial=True, required=False)

    fields_before_formset = get_trip_form_fields(before_formsets=True)
    fields_after_formset = get_trip_form_fields(after_formsets=True) + ['author_in', ]

    class Meta:
        model = Trip
        fields = get_trip_form_fields()

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        self.category = kwargs.pop('category', None)
        self.price_type = kwargs.pop('price_type', None)
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['trip_type'].empty_label = None
        self.fields['city'].queryset = City.objects.common_related()
        for field in self.fields.values():
            if not field.help_text:
                # place help_text tag to render fields with save height
                field.help_text = '&nbsp;'
        if self.price_type == Trip.PRICE_TYPE.noncom\
          or (self.price_type is None and self.instance and self.instance.is_noncom):
            del self.fields['price']
            del self.fields['currency']
        else:
            self.fields['currency'].empty_label = None

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < get_today():
            raise forms.ValidationError(self.trip_errors['low_date'])
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if end_date < get_today():
            raise forms.ValidationError(self.trip_errors['low_date'])
        return end_date

    def clean(self):
        clnd = self.cleaned_data
        if self.is_valid():
            if clnd['start_date'] > clnd['end_date']:
                raise forms.ValidationError(self.trip_errors['end_less_start_date'])
            if clnd['people_count'] > clnd['people_max_count']:
                raise forms.ValidationError(self.trip_errors['people_max_count'])
            if clnd['end_people_date'] > clnd['start_date']:
                raise forms.ValidationError(self.trip_errors['end_people_date'])
            if self.category and self.price_type:
                step_one_form = TripCreateStepOne(data={
                    'category': self.category,
                    'price_type': self.price_type})
                if not step_one_form.is_valid():
                    for err_msg in itertools.chain(step_one_form.errors.values()):
                        raise forms.ValidationError(err_msg)
        return clnd

    def save(self, commit=True):
        obj = super(TripForm, self).save(commit)
        if self.owner:
            obj.owner = self.owner
        if self.category is not None:
            obj.category = self.category
        if self.price_type is not None:
            obj.price_type = self.price_type
        if commit:
            obj.save()
        if obj.pk:
            if self.cleaned_data.get('author_in', False):
                obj.people.add(obj.owner)
        return obj


class TripUpdateForm(TripForm):
    images_to_delete = forms.ModelMultipleChoiceField(queryset=None, required=False)
    manual_fields = ('images_to_delete', )

    def __init__(self, *args, **kwargs):
        super(TripUpdateForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'instance'):
            self.fields['images_to_delete'].queryset = self.instance.images.all()

    def clean(self):
        super(TripUpdateForm, self).clean()
        if self.is_valid():
            # check, that images_to_delete belongs to current trip
            im_to_d = self.cleaned_data['images_to_delete']
            trip_imgs_len = self.instance.images.filter(
                pk__in=map(lambda x: x.pk, im_to_d)).count()
            if trip_imgs_len != len(im_to_d):
                raise forms.ValidationError(u'Неверное изображение')
        return self.cleaned_data

    def save(self, commit=True):
        obj = super(TripUpdateForm, self).save(commit)
        self.cleaned_data['images_to_delete'].delete()
        return obj

    class Meta:
        model = Trip
        fields = get_trip_form_fields() + ['images_to_delete', ]


class TripRequestForm(forms.ModelForm):
    trip_errors = {
        'already_in': u"Вы уже состоите в участниках поездки",
        'already_requested': u"Вы уже подали заявку в поездку",
        'already_started': u"Поездка уже началась",
        'already_finished': u"Поездка уже закончилась",
        'recruit_finished': u"Набор в поездку уже завершен",
    }

    class Meta:
        model = TripRequest
        fields = 'trip',

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        data = kwargs.get('data', None)
        if data:
            self.cancel = 'cancel' == data.get('action', None)
        else:
            self.cancel = False
        self.trip_request = None
        super(TripRequestForm, self).__init__(*args, **kwargs)
        self.fields['trip'].widget = forms.HiddenInput()

    def clean(self):
        if self.is_valid() and not self.cancel:
            trip = self.cleaned_data['trip']
            if trip.is_now():
                raise forms.ValidationError(self.trip_errors['already_started'])
            if trip.is_finished():
                raise forms.ValidationError(self.trip_errors['already_finished'])
            if trip.is_user_in(self.user):
                raise forms.ValidationError(self.trip_errors['alread_in'])
            if trip.is_user_has_request(self.user):
                raise forms.ValidationError(self.trip_errors['already_requested'])
            if trip.is_recruit_finished():
                raise forms.ValidationError(self.trip_errors['recruit_finished'])
        return self.cleaned_data

    def save(self, commit=True):
        trip = self.cleaned_data['trip']
        obj = None
        if self.cancel:
            for tr in TripRequest.objects.active()\
                                            .filter(trip=trip, user=self.user):
                tr.cancel()
            trip.notify_owner_about_cancel_request(self.user)
            if trip.is_closed():
                trip.notify_members_about_cancel_request(self.user)
            trip.people.remove(self.user)
        else:
            if trip.is_open():
                trip.people.add(self.user)
                self.user.notify_about_approve(trip)
                self.user.post_approve_on_fb_wall(trip)
            else:
                obj = super(TripRequestForm, self).save(commit)
                obj.user = self.user
                #TODO: respect commit arg
                obj.save()
            trip.notify_owner_about_request(self.user)
            if trip.is_closed():
                trip.notify_members_about_request(self.user)
        return obj


class TripFilterForm(forms.Form):
    AGES = (
        (20, 20),
        (25, 25),
        (30, 30),
        (35, 35),
        (40, 40),
        (45, 45),
        (50, 50),
    )

    month_year = forms.CharField(max_length=10, required=False)
    country = forms.ModelChoiceField(queryset=Country.objects.all(),
        empty_label=u"Не важно", required=False)
    price_type = forms.ChoiceField(required=False,
        choices=[("", u"Не важно"), ]+Trip.PRICE_TYPE._choices)
    gender = forms.ChoiceField(choices=[("", u"Не важно"), ]+User.GENDERS._choices, required=False)
    age_from = forms.ChoiceField(choices=AGES, initial=AGES[0][0], required=False)
    age_to = forms.ChoiceField(choices=AGES, initial=AGES[-1][0], required=False)
    users = forms.ModelChoiceField(queryset=None, required=False)
    category = forms.ModelChoiceField(queryset=None, required=False,
        empty_label=u"выберите категорию")

    def __init__(self, *args, **kwargs):
        users_queryset = kwargs.pop('users_queryset')
        category_queryset = kwargs.pop('category_queryset')
        super(TripFilterForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = users_queryset
        self.fields['category'].queryset = category_queryset

    def clean_month_year(self):
        month_year = self.cleaned_data['month_year']
        if month_year:
            try:
                datetime.strptime('01.' + month_year, '%d.%m.%Y')
            except ValueError:
                raise forms.ValidationError(u"Неверный формат даты")
        return month_year

    def _clean_age(self, age):
        if age:
            try:
                age = int(age)
            except ValueError:
                raise forms.ValidationError(u"Неверный формат возраста")
        return age

    def clean_age_from(self):
        return self._clean_age(self.cleaned_data['age_from'])

    def clean_age_to(self):
        return self._clean_age(self.cleaned_data['age_to'])

    def normalize_initial(self, initial):
        if not initial.get('age_from', None):
            initial['age_from'] = self.AGES[0][0]
        if not initial.get('age_to', None):
            initial['age_to'] = self.AGES[-1][0]
        return initial

    def get_normalized_initial(self):
        if self.is_valid():
            return self.normalize_initial(self.cleaned_data)
        return {}


class TripProcessForm(forms.Form):
    APPROVE, DENY = '0', '1'
    APPROVE_CHOICES = (
        (APPROVE, APPROVE),
        (DENY, DENY),
    )

    request_errors = {
        'bad_request': u'Неверная заявка',
        'bad_user': u'У вас нет прав на это действие',
    }

    request_pk = forms.IntegerField()
    action = forms.ChoiceField(choices=APPROVE_CHOICES)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TripProcessForm, self).__init__(*args, **kwargs)

    def clean_request_pk(self):
        request_pk = self.cleaned_data['request_pk']
        try:
            self.trip_request = TripRequest.objects\
                .active()\
                .select_related_trips()\
                .get(pk=request_pk)
        except TripRequest.DoesNotExist:
            raise forms.ValidationError(self.request_errors['bad_request'])
        trip = self.trip_request.trip
        if trip.is_invite():
            if trip.owner != self.user:
                raise forms.ValidationError(self.request_errors['bad_user'])
        elif trip.is_closed():
            if trip.people.filter(pk=self.user.pk).count() == 0\
                    and not trip.owner==self.user:
                raise forms.ValidationError(self.request_errors['bad_user'])

    def apply_action(self):
        if self.is_valid():
            action = self.cleaned_data['action']
            if action == TripProcessForm.APPROVE:
                self.trip_request.approve(self.user)
            else:
                self.trip_request.deny(self.user)
            return self.trip_request
        return None


class TripPointForm(forms.ModelForm):
    currency = forms.ChoiceField(label=u"Валюта",
        choices=TripPoint.CURRENCY._choices)

    auto_fields = 'trip',

    class Meta:
        model = TripPoint
        fields = 'title', 'description', 'link', 'price', 'currency', 'trip'
    
    def __init__(self, *args, **kwargs):
        self.point_type = kwargs.pop('point_type', None)
        self.price_type = kwargs.pop('price_type', None)
        super(TripPointForm, self).__init__(*args, **kwargs)
        if self.price_type == Trip.PRICE_TYPE.comm:
            del self.fields['price']
            del self.fields['currency']
            self.contains_price = False
        elif self.price_type is not None:
            self.fields['price'].required = True
            self.fields['currency'].required = True
            self.contains_price = True
        self.fields['title'].help_text = None
        if self.point_type:
            self.fields['title'].label = self.point_type.point_title_name

    def show_title(self):
        title = u''
        if self.point_type is not None:
            title = self.point_type.get_title()
        else:
            l.warning('{0}.show_title is called without provided "point_type"'.format(
                self.__class__.__name__))
        return title

    @property
    def is_blanked(self):
        for field_name in filter(lambda x: x not in self.auto_fields, self.fields):
            if field_name in self.cleaned_data and self.cleaned_data[field_name]:
                return False
        return True

    @property
    def is_many(self):
        if self.point_type:
            return self.point_type.many
        return False

    def save(self, commit=True):
        obj = super(TripPointForm, self).save(commit=False)
        obj.p_type = self.point_type
        if commit:
            obj.save()
        return obj
