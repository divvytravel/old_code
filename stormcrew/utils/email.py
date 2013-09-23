# -*- coding: utf-8 -*-
import logging
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import get_current_site
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_email_alternatives(subject, text, html, from_email, to):
    try:
        msg = EmailMultiAlternatives(subject, text, from_email, to)
        msg.attach_alternative(html, "text/html")
        msg.send()
    except:
        logger.exception("send_mail failed.")


def get_email_common_data(trip, user_requested):
    return {
        'trip': trip,
        'user_requested': user_requested,
        'domain': "http://" + str(get_current_site(None)),
    }, settings.EMAIL_HOST_USER


def send_common_email(user, trip, subject, template_base_name, email_to, context={}):
    base_context, from_email = get_email_common_data(trip, user)
    base_context.update(context)
    context = base_context
    template_html = "emails/{0}.html".format(template_base_name)
    template_txt = "emails/{0}.txt".format(template_base_name)
    text_content = render_to_string(template_html, context)
    html_content = render_to_string(template_txt, context)
    send_email_alternatives(
        subject, text_content, html_content, from_email, email_to)
