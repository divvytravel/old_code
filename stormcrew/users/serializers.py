# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    get_avatar_url = serializers.Field(source='get_avatar_url')
    get_full_name = serializers.Field(source='get_full_name')
    pk = serializers.Field(source='pk')

    class Meta:
        model = User


