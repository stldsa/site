from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from rest_framework import permissions

from events.models import Event


class EventsView(TemplateView):
    template_name = "events/event_list.html"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EventDetailView(DetailView):
    model = Event
    pk_url_kwarg = "id"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
