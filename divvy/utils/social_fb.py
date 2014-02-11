# -*- coding: utf-8 -*-
import logging
import facebook
from django.template.loader import render_to_string
from django.conf import settings
from .helpers import get_domain

logger = logging.getLogger(__name__)


def post_on_fb_wall(user, trip):
    message = render_to_string('social/facebook/new_trip.txt', {
        "trip": trip,
        "domain": get_domain()
    })
    if settings.FACEBOOK_SKIP_POST_ON_WALL:
        logger.debug(message)
    else:
        graph = facebook.GraphAPI(user.social_auth_response['access_token'])
        try:
            graph.put_object("me", "feed", message=message.encode('utf-8'))
        except facebook.GraphAPIError:
            logger.exception("Post to user's facebook timeline failed")
