# -*- coding: utf-8 -*-
from django import forms

from .models import User


class UserForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = ("first_name", "last_name", "birthday", "gender")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, forms.fields.ChoiceField):
                field.widget.attrs.update({'disabled': True})
            else:
                field.widget.attrs.update({'readonly': True})

    def clean(self):
        # currently userform is readonly
        raise forms.ValidationError(u"Эти данные изменить нельзя")
