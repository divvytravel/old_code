# -*- coding: utf-8 -*-
import logging
from django.conf import settings


class RequireLocalTrue(logging.Filter):
    def filter(self, record):
       return settings.LOCAL
