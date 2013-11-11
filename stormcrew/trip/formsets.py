# -*- coding: utf-8 -*-
from django.forms.models import BaseInlineFormSet
from django import forms


class TripPointInlineFormSet(BaseInlineFormSet):
    text_errors = {
        'blanked': u"Необходимо заполнить хотя бы одну позицию"
    }

    def clean(self):
        if not self.forms or self.forms[0].is_blanked:
            raise forms.ValidationError(self.text_errors['blanked'])

