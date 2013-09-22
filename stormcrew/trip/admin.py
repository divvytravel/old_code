# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Trip, TripPicture, TripRequest


class TripAdmin(admin.ModelAdmin):
    list_display = 'title', 'get_country', 'city', 'start_date', 'end_date'

    def get_country(self, obj):
        try:
            return u"{0}".format(obj.country)
        except:
            return u"-"
    get_country.short_description = u"Страна"


class TripPictureAdmin(admin.ModelAdmin):
    pass


class TripRequestAdmin(admin.ModelAdmin):
    list_display = 'trip', 'user', 'date_created', 'status'


admin.site.register(Trip, TripAdmin)
admin.site.register(TripPicture, TripPictureAdmin)
admin.site.register(TripRequest, TripRequestAdmin)
