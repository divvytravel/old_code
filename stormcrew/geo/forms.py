from django import forms
from trip.models import Trip


class CheapostFlightForm(forms.Form):
    origin = forms.CharField(max_length=5) #IATA
    destination = forms.CharField(max_length=5) #IATA
    departure_at = forms.DateField()
    return_at = forms.DateField()
    currency = forms.ChoiceField(choices=Trip.CURRENCY._choices)

    def get_currency_display(self):
        if self.is_valid():
            # TODO
            return self.cleaned_data['currency']
