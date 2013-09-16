# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Trip, TripPicture, TripRequest


class TripAdmin(admin.ModelAdmin):
    list_display = 'title', 'country', 'city', 'start_date', 'end_date'


class TripPictureAdmin(admin.ModelAdmin):
    pass


class TripRequestAdmin(admin.ModelAdmin):
    list_display = 'trip', 'user', 'date_created'


admin.site.register(Trip, TripAdmin)
admin.site.register(TripPicture, TripPictureAdmin)
admin.site.register(TripRequest, TripRequestAdmin)
