# -*- coding: utf-8 -*-
from django import forms
from django.utils import timezone
from .models import Trip


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
