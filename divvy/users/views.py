# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, DetailView

from braces.views import LoginRequiredMixin

from .forms import UserForm
from .models import User


class UserDetailView(DetailView):
    context_object_name = 'crew_user'
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class UserUpdateView(LoginRequiredMixin, UpdateView):

    form_class = UserForm
    model = User

    def get_success_url(self):
        return reverse("users:detail",
                    kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)
