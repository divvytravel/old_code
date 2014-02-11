from django import template

register = template.Library()

def is_approved_by(instance, user):
    # TODO
    # attach this to query set, using raw sql query. This will apply
    # db call to each trip request
    return instance.is_approved_by(user)

register.filter(is_approved_by)
