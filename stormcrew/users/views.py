# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import ListView

from braces.views import LoginRequiredMixin

from .forms import UserForm
from .models import User
from trip.models import Trip


class UserDetailView(DetailView):
    context_object_name = 'crew_user'
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        user = self.get_object()
        context.update({
            'trips_in': Trip.objects.with_people(user).count_gender(),
            'trips_created': Trip.objects.filter(owner=user).count_gender(),
        })
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):

    form_class = UserForm

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                    kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)
