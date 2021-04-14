from events.api.serializers import EventSerializer
from rest_framework import viewsets, permissions
import json
from django.http import HttpResponse
from action_network import get_events
from config.settings.local import ACTIONNETWORK_API_KEYS
from events.models import Event


def replace_id_key(event):
    event["id"] = event.pop("identifiers")
    event["start"] = event.pop("start_date")
    event["url"] = event.pop("browser_url")
    event = {
        key: value
        for key, value in event.items()
        if key in ["id", "title", "start", "url"]
    }
    return event


def list(request):
    all_events = []
    for api_key in ACTIONNETWORK_API_KEYS:
        events = get_events(api_key)
        events = [replace_id_key(event) for event in events]
        all_events += events
    return HttpResponse(json.dumps(all_events), content_type="application/json")


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
