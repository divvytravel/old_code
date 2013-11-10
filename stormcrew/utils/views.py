from django.contrib import messages


class SuccessMessageMixin(object):
    success_message = None

    def __init__(self, *args, **kwargs):
        super(SuccessMessageMixin, self).__init__(*args, **kwargs)
        self.is_success_message_set = False

    def get_success_message(self):
        return self.success_message

    def set_success_message(self):
        if not self.is_success_message_set:
            if self.get_success_message():
                messages.success(self.request, self.get_success_message())
            self.is_success_message_set = True

    def form_valid(self, form):
        self.set_success_message()
        return super(SuccessMessageMixin, self).form_valid(form)

    def delete(self, *args, **kwargs):
        self.set_success_message()
        return super(SuccessMessageMixin, self).delete(*args, **kwargs)
