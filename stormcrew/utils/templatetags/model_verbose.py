from django import template

register = template.Library()

def field_verbose(instance, field_name):
    """
    show verbose_name of a field
    """
    return instance._meta.get_field(field_name).verbose_name.capitalize()

register.filter(field_verbose)
