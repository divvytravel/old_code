# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, CreateView
from django.core.urlresolvers import reverse

from braces.views import LoginRequiredMixin

from users.models import User
from .forms import TripForm
from .models import Trip
from utils.views import SuccessMessageMixin


class TripFilterFormView(TemplateView):
    template_name = "trip/filter.html"

    def get_context_data(self, *args, **kwargs):
        return {
            'trip_users': User.objects.ready_to_trip().all()[:5]
        }


class TripCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TripForm
    model = Trip
    success_message = u"Поездка создана!"

    def post(self, *args, **kwargs):
        import pdb; pdb.set_trace()
        return super(TripCreateView, self).post(*args, **kwargs)

    def get_success_url(self):
        return reverse('home')
