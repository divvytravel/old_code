# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
    from django.contrib.auth import get_user_model  # Django 1.5
except ImportError:
    from postman.future_1_5 import get_user_model
from django.template import Library
# from django.utils.translation import ugettext_lazy as _

from postman.models import get_user_representation

register = Library()


##########
# filters
##########

from postman.templatetags.postman_tags import *

@register.filter
def or_me(value, arg):
    """
    Replace the value by a fixed pattern, if it equals the argument.

    Typical usage: message.obfuscated_sender|or_me:user

    """
    user_model = get_user_model()
    if not isinstance(value, (unicode, str)):
        value = (get_user_representation if isinstance(value, user_model) else unicode)(value)
    if not isinstance(arg, (unicode, str)):
        arg = (get_user_representation if isinstance(arg, user_model) else unicode)(arg)
    return u"Я" if value == arg else value

