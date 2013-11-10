# -*- coding: utf-8 -*-
from django.conf import settings


def custom_settings(request):
    return {
        "fill_test_data": settings.FILL_TEST_DATA,
        "cache_bootstrap": settings.CACHE_BOOTSTRAP,
    }
