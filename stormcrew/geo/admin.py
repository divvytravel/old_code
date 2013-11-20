# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Country, City, AirportIATA, UploadIATA


class CountryAdmin(admin.ModelAdmin):
    list_display = 'name',


class CityAdmin(admin.ModelAdmin):
    list_display = 'name', "country"


class AirportIATAAdmin(admin.ModelAdmin):
    list_display = 'iata', 'name_en', 'name_ru', 'parent_name_en'
    search_fields = 'name_en', 'name_ru', 'parent_name_en'


class UploadIATAAdmin(admin.ModelAdmin):
    list_display = 'csv_file', 'result'
    readonly_fields = 'result', 'error_details'


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(AirportIATA, AirportIATAAdmin)
admin.site.register(UploadIATA, UploadIATAAdmin)
