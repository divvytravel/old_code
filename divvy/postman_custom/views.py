from django.contrib.messages import get_messages

from postman.views import WriteView
from braces.views import AjaxResponseMixin, JSONResponseMixin


class AjaxWriteView(JSONResponseMixin, AjaxResponseMixin, WriteView):
    content_type = "text/html"
    ajax_template_name = "postman/write_ajax.html"

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        else:
            return super(AjaxWriteView, self).get_template_names()

    def form_valid(self, form):
        self.form_instance = form
        return super(AjaxWriteView, self).form_valid(form)

    def form_invalid(self, form):
        self.form_instance = form
        return super(AjaxWriteView, self).form_invalid(form)

    def post_ajax(self, request, *args, **kwargs):
        super(AjaxWriteView, self).post(request, *args, **kwargs)
        form = getattr(self, 'form_instance')
        resp = {}
        if form:
            if form.is_valid():
                resp['result'] = "success"
                resp['messages'] = [m.message for m in get_messages(request)]
            else:
                resp['result'] = "form_error"
                resp['errors'] = form.errors
        else:
            resp['result'] = "internal_error"
        return self.render_json_response(resp)
