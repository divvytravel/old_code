# -*- coding: utf-8 -*-
from django.views.generic import FormView, CreateView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.core import serializers

from braces.views import LoginRequiredMixin, AjaxResponseMixin,\
    JSONResponseMixin

from users.models import User
from .forms import TripForm, TripRequestForm, TripFilterForm
from .models import Trip, TripPicture
from utils.views import SuccessMessageMixin
from utils.helpers import wrap_in_iterable


# class TripFilterFormView(FormView):
class TripFilterFormView(JSONResponseMixin, AjaxResponseMixin, FormView):
    template_name = "trip/filter.html"
    form_class = TripFilterForm
    content_type = "text/html"

    def get_form_kwargs(self):
        kwargs = super(TripFilterFormView, self).get_form_kwargs()
        kwargs.update({
            'users_queryset': User.objects.ready_to_trip().all(),
        })
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(TripFilterFormView, self).get_context_data(*args, **kwargs)
        if 'GET' in self.request.method:
            context.update({
                'trips': Trip.objects.actual().count_gender().all()[:30],
            })
        return context

    def get_filtered_trips(self, form):
        clnd = form.cleaned_data
        return Trip.objects.actual()\
            .in_month_year(clnd['month_year'])\
            .in_country(clnd['country'])\
            .with_people_gender(clnd['gender'])\
            .with_people_age(clnd['age_from'], clnd['age_to'])\
            .with_people(clnd['users'])\
            .count_gender()

    def get_filtered_users(self, form, trips):
        clnd = form.cleaned_data
        return User.objects.ready_to_trip()\
            .in_trips(trips)\
            .with_age(clnd['age_from'], clnd['age_to'])\
            .with_gender(clnd['gender'])

    def set_filtered_users(self, form, trips):
        clnd = form.cleaned_data
        form.fields['users'].queryset =\
            User.objects.ready_to_trip()\
                .in_trips(trips)\
                .with_age(clnd['age_from'], clnd['age_to'])\
                .with_gender(clnd['gender'])

    def form_valid(self, form, ajax=False):
        trips = self.get_filtered_trips(form)
        users = self.get_filtered_users(form, trips)
        if ajax:
            return trips, users
        else:
            form.fields['users'].queryset = users
            return self.render_to_response(self.get_context_data(
                form=form,
                selected_users=wrap_in_iterable(form.cleaned_data['users']),
                trips=trips,
            ))

    def post_ajax(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            trips, users = self.form_valid(form, ajax=True)
            trips = serializers.serialize("json", trips)
            users = serializers.serialize("json", users)
            data = {
                'trips': trips,
                'users': users,
            }
        else:
            # TODO
            data = {}
        return self.render_json_response(data)

    def form_invalid(self, form):
        return super(TripFilterFormView, self).form_invalid(form)


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

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            messages.warning(self.request, u"Теперь вы можете подать заявку.")
            return HttpResponseRedirect("{0}?next={1}".format(
                settings.LOGIN_URL, self.request.path))
        return super(TripRequestFormView, self).post(*args, **kwargs)

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
        trip = self.get_trip()
        user_in = trip.is_user_in(self.request.user)
        if user_in:
            user_has_request = False
        else:
            user_has_request =  trip.is_user_has_request(self.request.user)
        try:
            country = trip.country
        except:
            country = u""
        context.update({
            "trip": trip,
            "trip_country": country,
            "user_in": user_in,
            "user_has_request": user_has_request,
        })
        return context

    def get_success_message(self):
        trip = self.get_trip()
        if 'cancel' == self.request.POST.get('action'):
            return u'Заявка на поездку "{0}" отменена.'.format(trip.title)
        if trip.is_open():
            return u'Заявка подана успешно! Теперь вы участвуете в поездке "{0}".'\
                .format(trip.title)
        elif trip.is_invite():
            return u'Заявка подана успешно! Ваша заявку будет рассмотрена создателем поездки. Вы получите сообщение на email о результате.'
        elif trip.is_closed():
            return u'Заявка подана успешно! Ваша заявку будет рассмотрена участниками поездки. Вы получите сообщение на email о результате.'
        else:
            return u'Заявка подана успешно!'

    def get_success_url(self):
        return reverse('home')
