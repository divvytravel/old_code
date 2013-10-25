# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from .models import Trip, TripRequest
from users.models import User
from geo.models import Country
from utils.helpers import get_today


def get_trip_form_fields():
    return (
        'title',
        'start_date',
        'end_date',
        'country',
        'city',
        'price',
        'currency',
        'includes',
        'people_count',
        'descr_main',
        'descr_share',
        'descr_additional',
        'descr_company',
        'trip_type',
    )

class TripForm(forms.ModelForm):
    trip_errors = {
        'end_less_start_date': u"Конечная дата не может быть меньше начальной",
        'low_date': u"Дата не может быть меньше сегодняшней",
    }

    country = forms.CharField(label=u"Страна", max_length=100)
    author_in = forms.BooleanField(label=u"Я участвую в этой поездке",
        initial=True, required=False)

    class Meta:
        model = Trip
        fields = get_trip_form_fields()

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['currency'].empty_label = None
        self.fields['trip_type'].empty_label = None
        for field in self.fields.values():
            if not field.help_text:
                # place help_text tag to render fields with save height
                field.help_text = '&nbsp;'

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
        if self.is_valid():
            if self.cleaned_data['start_date'] > self.cleaned_data['end_date']:
                raise forms.ValidationError(self.trip_errors['end_less_start_date'])
            self.cleaned_data['country'] =\
                Country.objects.get_or_create_normalized(
                    name=self.cleaned_data['country'])
        else:
            self.cleaned_data['country'] = \
                Country.objects.get_normalized_or_none(
                    name=self.cleaned_data['country'])
        return self.cleaned_data

    def save(self, commit=False, wait=False):
        obj = super(TripForm, self).save(commit)
        if self.owner:
            obj.owner = self.owner
        obj.save()
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

    def save(self, commit=False):
        obj = super(TripUpdateForm, self).save(commit)
        self.cleaned_data['images_to_delete'].delete()
        return obj

    class Meta:
        model = Trip
        fields = get_trip_form_fields() + ('images_to_delete', )


class TripRequestForm(forms.ModelForm):
    trip_errors = {
        'already_in': u"Вы уже состоите в участниках поездки",
        'already_requested': u"Вы уже подали заявку в поездку",
        'already_started': u"Поездка уже началась",
        'already_finished': u"Поездка уже закончилась",
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
        return self.cleaned_data

    def save(self, commit=False):
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
    gender = forms.ChoiceField(choices=[("", u"Не важно"), ]+User.GENDERS._choices, required=False)
    age_from = forms.ChoiceField(choices=AGES, initial=AGES[0][0], required=False)
    age_to = forms.ChoiceField(choices=AGES, initial=AGES[-1][0], required=False)
    users = forms.ModelChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        users_queryset = kwargs.pop('users_queryset')
        super(TripFilterForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = users_queryset

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
