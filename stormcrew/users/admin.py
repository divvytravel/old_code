# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from social_auth.models import UserSocialAuth, Nonce, Association

from .models import User


class UserAdmin(admin.ModelAdmin):
    create_form_class = UserCreationForm
    update_form_class = UserChangeForm


admin.site.register(User, UserAdmin)

admin.site.unregister(UserSocialAuth)
admin.site.unregister(Nonce)
admin.site.unregister(Association)
