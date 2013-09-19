# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from django.utils import timezone
from .models import Trip, TripRequest
from users.models import User
from geo.models import Country


class TripForm(forms.ModelForm):
    trip_errors = {
        'end_less_start_date': u"Конечная дата не может быть меньше начальной",
        'low_date': u"Дата не может быть меньше сегодняшней",
    }

    country = forms.CharField(label=u"Страна", max_length=100)

    class Meta:
        model = Trip
        fields = (
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

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner')
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['currency'].empty_label = None
        self.fields['trip_type'].empty_label = None
        for field in self.fields.values():
            if not field.help_text:
                # place help_text tag to render fields with save height
                field.help_text = '&nbsp;'

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < timezone.now().date():
            raise forms.ValidationError(self.trip_errors['low_date'])
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if end_date < timezone.now().date():
            raise forms.ValidationError(self.trip_errors['low_date'])
        return end_date

    def clean(self):
        if self.is_valid():
            if self.cleaned_data['start_date'] > self.cleaned_data['end_date']:
                raise forms.ValidationError(self.trip_errors['end_less_start_date'])
            self.cleaned_data['country'] =\
                Country.objects.get_or_create_normalized(
                    name=self.cleaned_data['country'])
        return self.cleaned_data

    def save(self, commit=False):
        obj = super(TripForm, self).save(commit)
        obj.owner = self.owner
        obj.save()
        return obj


class TripRequestForm(forms.ModelForm):
    trip_errors = {
        'already_in': u"Вы уже состоите в участниках поездки",
        'already_requested': u"Вы уже подали заявку в поездку",
    }

    class Meta:
        model = TripRequest
        exclude = 'user', 'date_created'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TripRequestForm, self).__init__(*args, **kwargs)
        self.fields['trip'].widget = forms.HiddenInput()

    def clean(self):
        if self.is_valid():
            trip = self.cleaned_data['trip']
            if trip.is_user_in(self.user):
                raise forms.ValidationError(self['alread_in'])
            if trip.is_user_has_request(self.user):
                raise forms.ValidationError(self['already_requested'])
        return self.cleaned_data

    def save(self, commit=False):
        obj = super(TripRequestForm, self).save(commit)
        obj.user = self.user
        obj.save()
        trip = self.cleaned_data['trip']
        if trip.is_open():
            trip.people.add(self.user)
        trip.notify_owner_about_request(self.user)
        if trip.is_closed():
            trip.notify_members_about_request(self.user)
        return obj


class TripFilterForm(forms.Form):
    AGES = (
        ('', u"Не важно"),
        ('20-25', '20-25'),
        ('25-30', '25-30'),
        ('35-40', '35-40'),
        ('40-45', '40-45'),
        ('45-50', '45-50'),
    )

    month_year = forms.CharField(max_length=10, required=False)
    country = forms.ModelChoiceField(queryset=Country.objects.all(),
        empty_label=u"Не важно", required=False)
    gender = forms.ChoiceField(choices=[("", u"Не важно"), ]+User.GENDERS._choices, required=False)
    age = forms.ChoiceField(choices=AGES, required=False)
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

    def clean_age(self):
        age = self.cleaned_data['age']
        if age:
            try:
                age_from, age_to = map(int, age.split('-'))
            except ValueError:
                raise forms.ValidationError(u"Неверный формат возраста")
        else:
            age_from, age_to = None, None
        return age_from, age_to
