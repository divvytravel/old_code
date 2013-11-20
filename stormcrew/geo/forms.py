from django import forms
from relish.decorators import instance_cache
from trip.models import Trip
from api.aviasales import AviasalesManger


class CheapestFlightForm(forms.Form):
    origin_text = forms.CharField(max_length=100) #Text
    destination_iata = forms.CharField(max_length=5) #IATA
    departure_at = forms.DateField()
    return_at = forms.DateField()
    currency = forms.ChoiceField(choices=Trip.CURRENCY._choices)

    def get_origin_iata(self):
        if self.is_valid():
            # TODO
            return 'MOW'

    def get_cheapest_price(self):
        av = self.get_av()
        return av.get_cheapest_price(
            origin=self.get_origin_iata(),
            destination=self.cleaned_data['destination_iata'],
            departure_at=self.cleaned_data['departure_at'],
            return_at=self.cleaned_data['return_at'],
            currency=self.cleaned_data['currency'],
        )

    def get_cheapest_search_link(self):
        return self.get_av().get_cheapest_search_link(
            origin=self.get_origin_iata(),
            destination=self.cleaned_data['destination_iata'],
            departure_at=self.cleaned_data['departure_at'],
            return_at=self.cleaned_data['return_at'],
        )

    @instance_cache
    def get_av(self):
        return AviasalesManger()
