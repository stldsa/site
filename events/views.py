import requests
from django.shortcuts import render
from django.views.generic import ListView
from events.models import Event
from datetime import datetime
from django.conf import settings

# Create your views here.

def event_list(request):
    response = requests.get('https://actionnetwork.org/api/v2/events/', headers = {'OSDI-API-Token': settings.ACTIONNETWORK_API_KEY})
    events_json = response.json()
    events = events_json['_embedded']['osdi:events']
    upcoming_events = []
    for event in events:
        info = {}
        info['date'] = datetime.fromisoformat(event['start_date'][:-1]).date()
        info['start_time'] = datetime.fromisoformat(event['start_date'][:-1]).time()
        info['actionnetwork_url'] = event['browser_url']
        info['title'] = event['title']
        info['description'] = event['description']
        upcoming_events.append(info)
    upcoming_events = [event for event in upcoming_events if event['date'] >= datetime.today().date()]
    upcoming_events = sorted(upcoming_events, key=lambda x: x['date'])

    return render(request, 'events/event_list.html', {'upcoming_events':upcoming_events})