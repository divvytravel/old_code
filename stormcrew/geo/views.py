from django.http import Http404
from django.views.generic import FormView
from braces.views import AjaxResponseMixin, JSONResponseMixin
from .forms import CheapostFlightForm


class CheapestFlightView(JSONResponseMixin, AjaxResponseMixin, FormView):
    form_class = CheapostFlightForm

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        raise Http404

    def get_ajax(self, request, *args, **kwargs):
        raise Http404

    def post_ajax(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        data = {}
        if form.is_valid():
            data['result'] = 'success'
            data['price'] = "304 {0}".format(form.get_currency_display())
        else:
            data['result'] = 'no-data'
        return self.render_json_response(data)
