from django.db.models.query import QuerySet

COUNTRIES_ADOPT = {
    'Russian Federation': 'Russia',
}

class CountryQuerySet(QuerySet):
    pass


class CityQuerySet(QuerySet):

    def common_related(self):
        return self.select_related('country')


class AirportIATAQuerySet(QuerySet):

    def adopt_country(self, country):
        return COUNTRIES_ADOPT.get(country, country)

    def find_iata(self, country_en, city_en=None, city_ru=None):
        iata_codes = self.filter(
            parent_name_en=self.adopt_country(country_en))
        iata = None
        found = True
        if city_en:
            iata_codes = iata_codes.filter(name_en=city_en)
        elif city_ru:
            iata_codes = iata_codes.filter(name_ru=city_ru)
        else:
            found = False
        if found:
            try:
                iata = iata_codes[0].iata
            except IndexError:
                pass
        return iata
