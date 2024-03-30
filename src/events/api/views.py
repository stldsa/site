from events.api.serializers import EventSerializer
from rest_framework import viewsets
from events.models import Event
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        start = make_aware(parse_datetime(self.request.query_params.get("start")))
        end = make_aware(parse_datetime(self.request.query_params.get("end")))
        return (
            Event.objects.filter(start__range=(start, end))
            .exclude(title__icontains="members only")
            .exclude(title__icontains="test_event")
            .exclude(status__icontains="cancelled")
        )
