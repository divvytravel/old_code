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
            "if first form contains price, then all forms shall contain price"
            self.contains_price = True
            currency_set = set()
            for form in self.forms:
                currency = form.cleaned_data.get('currency', None)
                self.currency = currency
                if currency_set and currency not in currency_set:
                    raise forms.ValidationError(self.text_errors['currency'])
                currency_set.add(currency)

    # def get_queryset(self):
    #     ## See get_queryset method of django.forms.models.BaseModelFormSet
    #     if not hasattr(self, '_queryset'):
    #         self._queryset = self.queryset.filter(type__startswith='xyz'))
    #         if not self._queryset.ordered:
    #             self._queryset = self._queryset.order_by(self.model._meta.pk.name)                
    #     return self._queryset


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
