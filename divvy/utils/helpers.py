import collections
from django.utils import timezone
from django.contrib.sites.models import get_current_site
from dateutil.relativedelta import relativedelta


def get_today():
    return timezone.now().date()


def date_yearsago(years, from_date=None):
    if from_date is None:
        from_date = timezone.now()
    return (from_date - relativedelta(years=years)).date()


def is_iterable(obj):
    return isinstance(obj, collections.Iterable)


def wrap_in_iterable(obj):
    if not is_iterable(obj):
        obj = [obj, ]
    return obj


def get_domain(request=None):
    return "http://" + str(get_current_site(request))
