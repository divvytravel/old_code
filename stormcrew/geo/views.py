# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import FormView
from braces.views import AjaxResponseMixin, JSONResponseMixin
from .forms import CheapestFlightForm


class CheapestFlightView(JSONResponseMixin, AjaxResponseMixin, FormView):
    form_class = CheapestFlightForm

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        raise Http404

    def get_ajax(self, request, *args, **kwargs):
        raise Http404

    def post_ajax(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        data = {'result': u"Нет данных"}
        if form.is_valid():
            price = form.get_cheapest_price()
            if price:
                data['result'] = 'success'
                data['price'] = price
        return self.render_json_response(data)
