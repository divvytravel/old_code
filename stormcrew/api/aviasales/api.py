# -*- coding: utf-8 -*-
import logging
import requests
from django.conf import settings

l = logging.getLogger('api_aviasales')


class AviasalesManger(object):
    api_url = 'http://api.aviasales.ru/v1'
    # TODO: avoid repeating currency codes
    currency_dict = {
        'euro': 'EUR',
        'rub': 'RUB',
        'dollar': 'USD',
    }

    def __init__(self):
        self.token = settings.TRAVELPAYOUTS_TOKEN
        self.marker = settings.TRAVELPAYOUTS_MARKER

    def convert_currency(self, currency):
        return self.currency_dict.get(currency, 'EUR')

    def date_format(self, date):
        return date.strftime("%Y-%m-%d")

    def get_cheapest_price(self, origin, destination, departure_at, return_at, currency):
        url = '{base}/cities/{origin}/directions/{destination}/prices.json'\
            .format(base=self.api_url, origin=origin, destination=destination)
        payload = {
            'departure_at': self.date_format(departure_at),
            'return_at': self.date_format(return_at),
            'currency': self.convert_currency(currency),
            'token': self.token,
        }
        l.debug('request to {0}'.format(url))
        r = requests.get(url, params=payload)
        l.debug('request done to {0}'.format(r.url))
        l.debug('request body: {0}'.format(r.text))
        if r.status_code == requests.codes.ok:
            r_json = r.json()
            if r_json['success']:
                try:
                    min_price = min(
                        map(lambda x: x['price'], r_json['data'][destination].values()))
                    l.debug('Found min_price: "{0}"'.format(min_price))
                except:
                    l.exception("bad parsing of aviasales response")
                    min_price = None
                return min_price
        l.debug('response not success')
        return None
