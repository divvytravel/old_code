# -*- coding: utf-8 -*-
from django import forms
from django.utils import timezone
from .models import Trip, TripRequest
from users.models import User


class TripForm(forms.ModelForm):
    trip_errors = {
        'end_less_start_date': u"Конечная дата не может быть меньше начальной",
        'low_date': u"Дата не может быть меньше сегодняшней",
    }

    class Meta:
        model = Trip
        exclude = 'owner', 'people', 'potential_people'

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
    date = forms.DateField(required=False)
    where = forms.CharField(max_length=100, required=False)
    gender = forms.ChoiceField(choices=[("", u"Не важно"), ]+User.GENDERS._choices, required=False)
    age_from = forms.IntegerField(required=False)
    age_to = forms.IntegerField(required=False)
    users = forms.ModelMultipleChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        users_queryset = kwargs.pop('users_queryset')
        super(TripFilterForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = users_queryset

    def clean_where(self):
        where = self.cleaned_data['where']
        return where.strip()
