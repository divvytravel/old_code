# -*- coding: utf-8 -*-
from django.forms.models import BaseInlineFormSet
from django import forms


class TripPointInlineFormSet(BaseInlineFormSet):
    text_errors = {
        'blanked': u"Необходимо заполнить хотя бы одну позицию",
        'currency': u"Во всех позициях валюта должна быть одинаковой"
    }

    def clean(self):
        super(TripPointInlineFormSet, self).clean()
        if not self.forms or self.forms[0].is_blanked:
            raise forms.ValidationError(self.text_errors['blanked'])
        currency_set = set()
        if self.forms[0].contains_price:
            for form in self.forms:
                currency = form.cleaned_data.get('currency', None)
                if currency_set and currency not in currency_set:
                    raise forms.ValidationError(self.text_errors['currency'])
                currency_set.add(currency)


