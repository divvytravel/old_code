from django import template

register = template.Library()

def adopt_alert_tag(tag):
    if tag == 'error':
        return 'danger'
    return tag

register.filter(adopt_alert_tag)
