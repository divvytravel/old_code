import collections
from django.utils import timezone
from dateutil.relativedelta import relativedelta


def today():
    return timezone.now().date()


def date_yearsago(years, from_date=None):
    if from_date is None:
        from_date = timezone.now()
    return (from_date - relativedelta(years=years)).date()


def wrap_in_iterable(obj):
    if not isinstance(obj, collections.Iterable):
        obj = [obj, ]
    return obj