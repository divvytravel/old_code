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

    def get_form_kwargs(self):
        kwargs = super(CheapestFlightView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def post_ajax(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        data = {'result': u"Нет данных"}
        if form.is_valid():
            data['result'] = 'success'
            price = form.get_cheapest_price()
            if price:
                data['price'] = price
                data['price_result'] = u"success"
            else:
                data['price'] = 0
                data['price_result'] = u"Нет данных"
            data['search_link'] = form.get_cheapest_search_link()
        else:
            data['search_link'] = form.get_blanked_search_link()
        return self.render_json_response(data)
