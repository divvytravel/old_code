# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, CreateView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin

from users.models import User
from .forms import TripForm, TripRequestForm
from .models import Trip, TripPicture
from utils.views import SuccessMessageMixin


class TripFilterFormView(TemplateView):
    template_name = "trip/filter.html"

    def get_context_data(self, *args, **kwargs):
        return {
            'trip_users': User.objects.ready_to_trip().all()[:5],
            'trips': Trip.objects.actual().all()[:30]
        }


class TripCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TripForm
    model = Trip
    success_message = u"Поездка создана!"

    def get_form_kwargs(self):
        kwargs = super(TripCreateView, self).get_form_kwargs()
        kwargs.update({
            'owner': self.request.user,
        })
        return kwargs

    def save_images(self):
        for image_stream in self.request.FILES.getlist('files[]'):
            pic = TripPicture(file=image_stream, trip=self.object)
            pic.save()

    def get_success_url(self):
        self.save_images()
        return reverse('home')


class TripRequestFormView(SuccessMessageMixin, CreateView):
    form_class = TripRequestForm
    template_name = "trip/trip_request_detail.html"
    success_message = u"Поездка создана!"

    def get_trip(self):
        if not hasattr(self, '_trip_object'):
            setattr(self, '_trip_object',
                get_object_or_404(Trip, pk=self.kwargs['pk']))
        return self._trip_object

    def get_initial(self):
        initial = {
            'trip': self.get_trip(),
        }
        return initial

    def get_form_kwargs(self):
        kwargs = super(TripRequestFormView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TripRequestFormView, self).get_context_data(**kwargs)
        context.update({
            "trip": self.get_trip()
        })
        return context

    def get_success_url(self):
        return reverse('home')
