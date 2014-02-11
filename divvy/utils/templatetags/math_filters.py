from django.template.base import Library
register = Library()


@register.filter(is_safe=False)
def minus(value, arg):
    """Minus the arg from the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return ''
