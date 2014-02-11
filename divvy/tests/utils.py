from random import randrange
from datetime import datetime, timedelta

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    rd = start + timedelta(seconds=random_second)
    if hasattr(rd, 'date'):
        return rd.date()
    return rd


def random_actual_date():
    return random_date(
        datetime.now()+timedelta(days=1),
        datetime.now()+timedelta(days=50))
