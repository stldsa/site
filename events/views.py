from django.views.generic.base import TemplateView
from rest_framework import permissions


class EventsView(TemplateView):

    template_name = "events/event_list.html"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
