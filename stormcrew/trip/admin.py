# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Trip, TripPicture


class TripAdmin(admin.ModelAdmin):
    list_display = 'title', 'country', 'city', 'start_date', 'end_date'


class TripPictureAdmin(admin.ModelAdmin):
    pass


admin.site.register(Trip, TripAdmin)
admin.site.register(TripPicture, TripPictureAdmin)
