import logging
from django import forms
from django.conf import settings
from relish.decorators import instance_cache
from trip.models import Trip
from api.aviasales import AviasalesManger
from .models import AirportIATA

l_avia = logging.getLogger('api_aviasales')


class CheapestFlightForm(forms.Form):
    destination_iata = forms.CharField(max_length=5) #IATA
    departure_at = forms.DateField()
    return_at = forms.DateField()
    currency = forms.ChoiceField(choices=Trip.CURRENCY._choices)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CheapestFlightForm, self).__init__(*args, **kwargs)

    @instance_cache
    def get_origin_iata(self):
        request = self.request
        iata = None
        if request and settings.GEOIP_PATH:
            from django.contrib.gis.geoip import GeoIP
            ip_address = request.META.get('REMOTE_ADDR')
            g = GeoIP()
            city_info = g.city(ip_address) or dict()
            city = city_info.get('city', None)
            country = city_info.get('country_name', None)
            iata = AirportIATA.objects.find_iata(
                country_en=country,
                city_en=city,
            )
        if iata:
            l_avia.debug('Origin iata found: {0}'.format(iata))
            return iata
        else:
            l_avia.debug('Origin iata NOT found...')
            return 'MOW' # Moscow

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

    def get_blanked_search_link(self):
        return self.get_av().get_blanked_search_link()

    @instance_cache
    def get_av(self):
        return AviasalesManger()
