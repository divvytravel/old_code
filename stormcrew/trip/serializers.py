# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Trip, TripCategory


class TripSerializer(serializers.ModelSerializer):
    count_female = serializers.SerializerMethodField('get_count_female')
    count_male = serializers.SerializerMethodField('get_count_male')
    count_all_people = serializers.SerializerMethodField('get_count_all_people')

    start_date_format = serializers.Field(source='start_date_format')
    end_date_format = serializers.Field(source='end_date_format')
    end_people_date_format = serializers.Field(source='end_people_date_format')
    get_currency_display = serializers.Field(source='get_currency_display')
    get_absolute_url = serializers.Field(source='get_absolute_url')
    show_price_type = serializers.Field(source='show_price_type')
    show_people_places_left = serializers.Field(source='show_people_places_left')
    city_name = serializers.RelatedField(source='city')

    class Meta:
        model = Trip
        exclude = ('people', 'city')

    def get_count_female(self, obj):
        if hasattr(obj, 'count_female'):
            return obj.count_female
        return None

    def get_count_male(self, obj):
        if hasattr(obj, 'count_male'):
            return obj.count_male
        return None

    def get_count_all_people(self, obj):
        if hasattr(obj, 'count_all_people'):
            return obj.count_all_people
        return None


class TripCategorySerializer(serializers.ModelSerializer):
    pk = serializers.Field(source='pk')

    class Meta:
        model = TripCategory
