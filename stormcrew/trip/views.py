from django.views.generic import TemplateView
from users.models import User


class TripFilterFormView(TemplateView):
    template_name = "trip/filter.html"

    def get_context_data(self, *args, **kwargs):
        return {
            'trip_users': User.objects.ready_to_trip().all()[:5]
        }


