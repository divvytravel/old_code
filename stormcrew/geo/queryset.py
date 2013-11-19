from django.db.models.query import QuerySet


class CountryQuerySet(QuerySet):
    pass


class CityQuerySet(QuerySet):

    def common_related(self):
        return self.select_related('country')
