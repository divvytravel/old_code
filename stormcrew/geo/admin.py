# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Country, City


class CountryAdmin(admin.ModelAdmin):
    list_display = 'name',


class CityAdmin(admin.ModelAdmin):
    list_display = 'name', "country"


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
