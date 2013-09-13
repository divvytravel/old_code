# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Trip


class TripAdmin(admin.ModelAdmin):
    list_display = 'title', 'country', 'city', 'start_date', 'end_date'


admin.site.register(Trip, TripAdmin)
