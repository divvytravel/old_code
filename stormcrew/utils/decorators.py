from functools import wraps

def instance_cache(func):
    """
    Stores returned values as instance attr. On next call will return this attr.
    """
    @wraps(func)
    def wrapped(instance, *args, **kwargs):
        attr_name = "_{0}".format(func.__name__)
        if hasattr(instance, attr_name) and not kwargs.get('skip_cache', False):
            return getattr(instance, attr_name)
        else:
            value = func(instance, *args, **kwargs)
            setattr(instance, attr_name, value)
            return value
    return wrapped


def self_if_blank_arg(func):
    """
    If all of function kwargs are False in python way, then return self.
    Otherwise, return applied function
    """
    @wraps(func)
    def wrapped(instance, *args, **kwargs):
        if any(args) or any(kwargs.values()):
            return func(instance, *args, **kwargs)
        else:
            return instance
    return wrapped


def sort_trips_by_time_status(func):
    # TODO
    # apply sorting using db query
    @wraps(func)
    def wrapped(instance, *args, **kwargs):
        trips = func(instance, *args, **kwargs)
        return sorted(trips, key=lambda t: 1 if t.is_finished() else 0)
    return wrapped
