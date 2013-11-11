# -*- coding: utf-8 -*-
from django.views.generic import FormView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404

from braces.views import LoginRequiredMixin, AjaxResponseMixin,\
    JSONResponseMixin

from users.models import User
from users.serializers import UserSerializer, UserPkSerializer
from .forms import TripForm, TripRequestForm, TripFilterForm, TripUpdateForm,\
    TripProcessForm, TripCreateStepOne, TripPointForm
from .models import Trip, TripPicture, TripCategory, TripPoint, TripPointType
from .serializers import TripSerializer, TripCategorySerializer
from utils.views import SuccessMessageMixin
from utils.helpers import wrap_in_iterable, is_iterable
from relish.decorators import instance_cache

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet

class TripFilterFormView(JSONResponseMixin, AjaxResponseMixin, FormView):
    template_name = "trip/filter.html"
    form_class = TripFilterForm
    content_type = "text/html"

    def get(self, request, *args, **kwargs):
        if 'clear' in request.GET:
            self.clear_session_form_data()
            return HttpResponseRedirect(self.request.path)
        return super(TripFilterFormView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TripFilterFormView, self).get_form_kwargs()
        kwargs.update({
            'users_queryset': User.objects.ready_to_trip().have_trip().all(),
            'category_queryset': TripCategory.objects.all(),
        })
        if self.request.method == 'GET':
            self.udpate_form_kwargs_from_session(kwargs)
        return kwargs

    def udpate_form_kwargs_from_session(self, kwargs):
        session_form_data = self.get_session_form_data()
        if session_form_data:
            users = session_form_data.get('users', None)
            if users:
                session_form_data['users'] = users.pk

            country = session_form_data.get('country', None)
            if country:
                session_form_data['country'] = country.pk

            category = session_form_data.get('category', None)
            if category and isinstance(category, TripCategory):
                session_form_data['category'] = category.pk
            kwargs.setdefault('data', session_form_data)

    def get_context_data(self, *args, **kwargs):
        context = super(TripFilterFormView, self).get_context_data(*args, **kwargs)
        if 'GET' in self.request.method:
            form = context.get('form', None)
            if form is not None and form.is_valid():
                trips, users, selected_users, trip_categories = self.get_queries_data(form)
                form.fields['users'].queryset = users
                form.fields['category'].queryset = trip_categories
            else:
                trips = Trip.objects.actual().count_gender().all()[:30]
                selected_users = []
            context.update({
                'trips': trips,
                'selected_users': selected_users,
            })
        return context

    def get_session_form_data(self):
        return self.request.session.get('trip_form_data', {})

    def set_session_form_data(self, form, data=None):
        if data is None:
            data = form.get_normalized_initial()
        self.request.session['trip_form_data'] = data

    def clear_session_form_data(self):
        return self.request.session.pop('trip_form_data', None)

    def remove_user_from_session_form_data(self):
        session_form_data = self.get_session_form_data()
        session_form_data['users'] = []
        self.set_session_form_data(form=None, data=session_form_data)

    def get_initial(self):
        return self.get_session_form_data()

    def is_user_satisfy(self, user_pk, gender, age_from, age_to):
        if isinstance(user_pk, User):
            user = user_pk
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return False
        return user.is_satisfy(gender, age_from, age_to)

    def get_filtered_trips(self, form, category=True, count_gender=True):
        clnd = form.cleaned_data
        trip_qs = Trip.objects
        if count_gender:
            # have to apply count first. For some reason, if apply lately,
            # count will show bad values
            trip_qs = trip_qs.count_gender()
        trip_qs = trip_qs.actual()\
            .in_month_year_or_in_country(clnd['month_year'], clnd['country'])\
            .with_price_type(clnd['price_type'])\
            .with_people_gender(clnd['gender'])\
            .with_people_age(clnd['age_from'], clnd['age_to'])
        if category:
            trip_qs = trip_qs.with_category(clnd['category'])
        user_pk = clnd['users']
        if is_iterable(clnd['users']):
            try:
                user_pk = user_pk[0]
            except IndexError:
                user_pk = None
        if self.is_user_satisfy(user_pk, clnd['gender'],
                                        clnd['age_from'], clnd['age_to']):
            trip_qs = trip_qs.with_people(clnd['users'])
        else:
            self.remove_user_from_session_form_data()
        return trip_qs

    def get_filtered_users(self, form, trips):
        clnd = form.cleaned_data
        return User.objects.ready_to_trip().have_trip()\
            .in_trips(trips)\
            .with_age(clnd['age_from'], clnd['age_to'])\
            .with_gender(clnd['gender'])

    def get_filtered_categories(self, trips):
        return TripCategory.objects.filter(trips__in=trips)

    def get_queries_data(self, form):
        trips = self.get_filtered_trips(form)
        if not form.cleaned_data['category']:
            trips_for_categories = trips
        else:
            trips_for_categories = self.get_filtered_trips(form,
                category=False, count_gender=False)
        users = self.get_filtered_users(form, trips)
        trip_categories = self.get_filtered_categories(trips_for_categories)
        selected_users = wrap_in_iterable(form.cleaned_data['users'] or [])
        return trips, users, selected_users, trip_categories

    def form_valid(self, form, data_only=False):
        self.set_session_form_data(form)
        trips, users, selected_users, trip_categories = self.get_queries_data(form)
        if data_only:
            return trips, users, selected_users, trip_categories
        else:
            form.fields['users'].queryset = users
            form.fields['category'].queryset = trip_categories
            return self.render_to_response(self.get_context_data(
                form=form,
                selected_users=selected_users,
                trips=trips,
            ))

    def post_ajax(self, request, *args, **kwargs):
        if 'clear' in self.request.POST:
            self.clear_session_form_data()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            trips, users, selected_users, trip_categories = self.form_valid(form, data_only=True)
            if selected_users:
                selected_users = UserPkSerializer(selected_users).data
            trips = TripSerializer(trips, many=True).data
            users = UserSerializer(users, many=True).data
            trip_categories = TripCategorySerializer(trip_categories, many=True).data
            selected_category = form.cleaned_data['category']
            if is_iterable(selected_category):
                selected_category = selected_category[0]
            if selected_category:
                selected_category = selected_category.pk
            data = {
                'trips': trips,
                'users': users,
                'selected_users': selected_users,
                'trip_categories': trip_categories,
                'selected_category': selected_category,
            }
        else:
            # TODO
            data = {}
        return self.render_json_response(data)

    def form_invalid(self, form):
        return super(TripFilterFormView, self).form_invalid(form)


class SaveImagesMixin(object):
    def save_images(self):
        for image_stream in self.request.FILES.getlist('files[]'):
            pic = TripPicture(file=image_stream, trip=self.object)
            pic.save()


class TripCreateStepOneView(LoginRequiredMixin, FormView):
    template_name = 'trip/create_step_1.html'
    form_class = TripCreateStepOne

    def form_valid(self, form):
        self.price_type = form.cleaned_data['price_type']
        self.category = form.cleaned_data['category']
        return super(TripCreateStepOneView, self).form_valid(form)
        

    def get_success_url(self):
        return reverse('trip_create_step_two', kwargs={
            'price_type': self.price_type,
            'category_slug': self.category.slug})



class TripPointInline(InlineFormSet):
    max_num = 1
    extra = 1
    model = TripPoint
    form_class = TripPointForm
    point_type = None

    def __init__(self, *args, **kwargs):
        self.point_type = kwargs.pop('point_type', None)
        super(TripPointInline, self).__init__(*args, **kwargs)

    def get_extra_form_kwargs(self):
        return {
            'point_type': self.point_type,
            'price_type': self.view.price_type,
        }

    def get_formset_kwargs(self):
        kwargs = super(TripPointInline, self).get_formset_kwargs()
        if self.point_type:
            kwargs['prefix'] = self.point_type.get_form_prefix()
        return kwargs

    def get_factory_kwargs(self):
        kwargs = super(TripPointInline, self).get_factory_kwargs()
        if self.point_type:
            if self.point_type.many:
                kwargs['max_num'] = None
        kwargs['can_delete'] = False
        return kwargs


class TripCreateStepTwoView(LoginRequiredMixin, SuccessMessageMixin, CreateWithInlinesView,
                                                            SaveImagesMixin):
    form_class = TripForm
    model = Trip
    success_message = u"Поездка создана!"
    template_name = 'trip/create_step_2.html'

    def get_inlines(self):
        inlines = []
        for point_type in self.category.get_point_types():
            inlines.append((TripPointInline, {'point_type': point_type, }))
        return inlines

    def define_many_for_inline_formset(self, inline_formset, inline_kwargs):
        point_type = inline_kwargs.get('point_type', None)
        is_many = False
        if point_type:
            is_many = point_type.many
        setattr(inline_formset, 'is_many', is_many)
        setattr(inline_formset, 'id_for_many', "inline_many_{0}".format(point_type.pk))
        setattr(inline_formset, 'custom_prefix', point_type.get_form_prefix())
        setattr(inline_formset, 'form_css_class', point_type.get_form_css_class())

    def construct_inlines(self):
        """
        Returns the inline formset instances
        """
        inline_formsets = []
        for inline_class, inline_kwargs in self.get_inlines():
            inline_instance = inline_class(self.model, self.request, self.object, self.kwargs, self, **inline_kwargs)
            inline_formset = inline_instance.construct_formset()
            self.define_many_for_inline_formset(inline_formset, inline_kwargs)
            inline_formsets.append(inline_formset)
        return inline_formsets

    def get_form_kwargs(self):
        kwargs = super(TripCreateStepTwoView, self).get_form_kwargs()
        kwargs.update({
            'owner': self.request.user,
            'category': self.category,
            'price_type': self.price_type,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TripCreateStepTwoView, self).get_context_data(**kwargs)
        context['category'] = self.category
        #TODO get text from Trip.PRICE_TYPE
        if self.price_type == Trip.PRICE_TYPE.comm:
            context['price_type'] = u'коммерческая'
        else:
            context['price_type'] = u'некоммерческая'
        return context

    def get_success_url(self):
        self.set_success_message()
        self.save_images()
        return reverse('home')

    @property
    @instance_cache
    def category(self):
        return get_object_or_404(TripCategory, slug=self.kwargs['category_slug'])

    @property
    @instance_cache
    def price_type(self):
        price_type = self.kwargs['price_type']
        if price_type not in map(lambda x: x[0], Trip.PRICE_TYPE._choices):
            raise Http404
        return price_type


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
        next = self.request.POST.get('next', None)
        return next or reverse('home')


class TripUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView,
                                                            SaveImagesMixin):
    model = Trip
    form_class = TripUpdateForm
    template_name = "trip/trip_update.html"
    success_message = u"Поездка обновлена"

    def get_success_url(self):
        self.save_images()
        return self.object.get_absolute_url()

    def get_form_kwargs(self):
        if self.object.owner != self.request.user:
            raise PermissionDenied  # return a forbidden response
        kwargs = super(TripUpdateView, self).get_form_kwargs()
        return kwargs


class TripDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Trip
    success_message = u"Поездка удалена"
    success_url = reverse_lazy('users:cabinet')

    def get_object(self):
        obj = super(TripDeleteView, self).get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied
        return obj


class TripRequestApproveView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = TripProcessForm
    success_url = reverse_lazy('users:cabinet')

    def get(self, *args, **kwargs):
        raise PermissionDenied

    def get_form_kwargs(self):
        kwargs = super(TripRequestApproveView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.apply_action()
        self.form = form
        return super(TripRequestApproveView, self).form_valid(form)

    def form_invalid(self, form):
        for form_error in form.errors.values():
            messages.error(self.request, form_error)
        return HttpResponseRedirect(self.success_url)

    def get_success_message(self):
        form = getattr(self, 'form', None)
        if form is not None:
            if form.cleaned_data['action'] == TripProcessForm.APPROVE:
                return u"Заявка принята"
            else:
                return u"Заявка отклонена"
