from django.template.base import Library
register = Library()


@register.filter(is_safe=False)
def last_qs_item(list_var):
    """Return item from list with given index."""
    return list_var[len(list_var)-1]
