# -*- coding: utf-8 -*-
from django.contrib.auth.models import UserManager
from .queryset import UserQuerySet


class UserManagerWithFilters(UserManager):
    def get_query_set(self):
        return UserQuerySet(self.model)
    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)
