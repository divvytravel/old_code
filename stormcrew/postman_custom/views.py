from postman.views import WriteView
from braces.views import AjaxResponseMixin, JSONResponseMixin


class AjaxWriteView(JSONResponseMixin, AjaxResponseMixin, WriteView):
    content_type = "text/html"
    ajax_template_name = "postman/write_ajax.html"

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        else:
            return super(AjaxWriteView, self).get_template_names(self)
    # def get_ajax(self, request, *args, **kwargs):
    #     pass

    def post_ajax(self, request, *args, **kwargs):
        return self.render_json_response({"result": "ok"})
