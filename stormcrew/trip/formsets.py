# -*- coding: utf-8 -*-
from django.forms.models import BaseInlineFormSet
from django import forms

CURRENCY_ERROR = u"Валюта должна быть одинаковой во всех позициях"


class TripPointInlineFormSet(BaseInlineFormSet):
    text_errors = {
        'blanked': u"Необходимо заполнить хотя бы одну позицию",
        'currency': CURRENCY_ERROR
    }

    def clean(self):
        super(TripPointInlineFormSet, self).clean()
        if not self.forms or self.forms[0].is_blanked:
            raise forms.ValidationError(self.text_errors['blanked'])
        self.contains_price = False
        self.currency = None
        if self.forms[0].contains_price:
            self.contains_price = True
            currency_set = set()
            for form in self.forms:
                currency = form.cleaned_data.get('currency', None)
                self.currency = currency
                if currency_set and currency not in currency_set:
                    raise forms.ValidationError(self.text_errors['currency'])
                currency_set.add(currency)


class TripPointInlinesWrapper(list):
    text_errors = {
        'currency': CURRENCY_ERROR,
    }

    def clean(self):
        self._non_formset_errors = []
        if len(self) and self[0].contains_price:
            currency_set = set()
            for formset in self:
                if currency_set and formset.currency not in currency_set:
                    self._non_formset_errors.append(self.text_errors['currency'])
                    return False
                currency_set.add(formset.currency)
        return True

    def non_formset_errors(self):
        return getattr(self, '_non_formset_errors', [])
