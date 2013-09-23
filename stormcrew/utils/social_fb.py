# -*- coding: utf-8 -*-
import logging
import facebook
from django.template.loader import render_to_string
from .helpers import get_domain

logger = logging.getLogger(__name__)


def post_on_fb_wall(user, trip):
    graph = facebook.GraphAPI(user.social_auth_response['access_token'])
    message = render_to_string('social/facebook/new_trip.txt', {
        "trip": trip,
        "domain": get_domain()
    })
    try:
        graph.put_object("me", "feed", message=message.encode('utf-8'))
    except facebook.GraphAPIError:
        logger.exception("Post to user's facebook timeline failed")
