# -*- coding: utf-8 -*-
from django import forms
from .models import Trip


class TripForm(forms.ModelForm):

    class Meta:
        model = Trip

    def __init__(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['currency'].empty_label = None
        self.fields['trip_type'].empty_label = None
