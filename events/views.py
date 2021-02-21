import requests, pytz
from django.shortcuts import render
from django.views.generic.list import ListView
from events.models import Event, APICalls
from datetime import datetime
from django.conf import settings
from action_network import get_events


def update_events():
    last_api_call = APICalls.objects.order_by("-datetime")[0]
    last_api_call = last_api_call.datetime.isoformat()
    events = []
    for key in settings.ACTIONNETWORK_API_KEYS:
        response = get_events()
        tz = pytz.timezone("America/Chicago")
        chicago_now = datetime.now(tz)
        APICalls.objects.all().delete()
        APICalls(datetime=chicago_now).save()
        events += events_json["_embedded"]["osdi:events"]
    for event in events:
        obj, created = Event.objects.update_or_create(
            actionnetwork_id=event["identifiers"][0].split(":")[1],
            defaults={
                "title": event["title"],
                "date": datetime.fromisoformat(event["start_date"][:-1]).date(),
                "start_time": datetime.fromisoformat(event["start_date"][:-1]).time(),
                "actionnetwork_url": event["browser_url"],
                "description": event["description"],
            },
        )


class EventList(ListView):
    model = Event
    context_object_name = "upcoming_events"

    def get_queryset(self):
        update_events()
        return Event.objects.filter(date__gte=datetime.today().date()).order_by("date")


event_list = EventList.as_view()