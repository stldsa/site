from events.api.serializers import EventSerializer
from rest_framework import viewsets
from events.models import Event


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")
        return (
            Event.objects.filter(start__range=(start, end))
            .exclude(title__icontains="members only")
            .exclude(title__icontains="test_event")
        )
