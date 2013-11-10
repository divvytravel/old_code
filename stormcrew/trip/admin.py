# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Trip, TripPicture, TripRequest, TripCategory,\
    TripPointType, TripPoint


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


class TripPointTypeAdmin(admin.ModelAdmin):
    list_display = 'title', 'category'


class TripPointAdmin(admin.ModelAdmin):
    list_display = 'p_type', 'price', 'trip'


class TripCategoryAdmin(admin.ModelAdmin):
    list_display = 'title',
    prepopulated_fields = {"slug": ("title",)}


class TripRequestAdmin(admin.ModelAdmin):
    list_display = 'trip', 'user', 'date_created', 'status'


admin.site.register(Trip, TripAdmin)
admin.site.register(TripPicture, TripPictureAdmin)
admin.site.register(TripRequest, TripRequestAdmin)
admin.site.register(TripCategory, TripCategoryAdmin)
admin.site.register(TripPoint, TripPointAdmin)
admin.site.register(TripPointType, TripPointTypeAdmin)
