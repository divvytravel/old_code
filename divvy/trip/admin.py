# -*- coding: utf-8 -*-
from django.contrib import admin

from django.contrib.contenttypes import generic
from .models import Trip, TripRequest, TripCategory,\
    TripPointType, TripPoint, Tags, Images


class ImagesInline(generic.GenericStackedInline):
    model = Images
    extra = 1


class TripPointInline(admin.TabularInline):
    model = TripPoint
    extra = 0


class TripAdmin(admin.ModelAdmin):
    list_display = 'title', 'get_country', 'city', 'start_date', 'end_date'
    inlines = [ImagesInline, TripPointInline]

    def get_country(self, obj):
        try:
            return u"{0}".format(obj.country)
        except:
            return u"-"
    get_country.short_description = u"Страна"


class TripPointTypeAdmin(admin.ModelAdmin):
    list_display = 'title', 'category', 'many'


class TripPointAdmin(admin.ModelAdmin):
    list_display = 'p_type', 'price', 'trip'


class TripCategoryAdmin(admin.ModelAdmin):
    list_display = 'title',
    prepopulated_fields = {"slug": ("title",)}


def make_approved(modeladmin, request, queryset):
    for item in queryset.all():
        item.approve(request.user)
make_approved.short_description = "Approve selected requests"

class TripRequestAdmin(admin.ModelAdmin):
    list_display = 'trip', 'user', 'date_created', 'status'
    actions = [make_approved]

admin.site.register(Trip, TripAdmin)
admin.site.register(TripRequest, TripRequestAdmin)
admin.site.register(TripCategory, TripCategoryAdmin)
admin.site.register(TripPoint, TripPointAdmin)
admin.site.register(TripPointType, TripPointTypeAdmin)
admin.site.register(Tags)
