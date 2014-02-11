# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from social_auth.backends.facebook import FacebookBackend
from users.models import User

logger = logging.getLogger(__name__)

def get_facebook_avatar_url(fb_user_id):
    return "http://graph.facebook.com/{id}/picture".format(id=fb_user_id)


def get_facebook_birthday(response):
    birthday = response.get('birthday', None)
    if birthday:
        try:
            birthday = datetime.strptime(birthday, "%m/%d/%Y").date()
        except ValueError:
            logger.warning(
                "Unknown facebook birthday format: '{0}'".format(birthday))
            birthday = None
    return birthday


def get_facebook_gender(response):
    gender = response.get('gender', None)
    if gender:
        if u'жен' in gender or 'female' in gender:
            gender = User.GENDERS.female
        elif u'муж' in gender or 'male' in gender:
            gender = User.GENDERS.male
    return gender


def store_additional_fields(*args, **kwargs):
    backend = kwargs['backend']
    details = kwargs.get('details', {})
    response = kwargs['response']
    if isinstance(backend, FacebookBackend):
        details.update({
            'avatar_url': get_facebook_avatar_url(kwargs['uid']),
            'social_auth_response': response,
            'provider': User.PROVIDERS.facebook,
        })
        birthday = get_facebook_birthday(response)
        if birthday:
            details.update({"birthday": birthday})
        gender = get_facebook_gender(response)
        if gender:
            details.update({"gender": gender})
    return {'details': details}
