from django.shortcuts import render
from django.views.generic import ListView
from events.models import Event
from datetime import datetime

# Create your views here.
class EventList(ListView):
    queryset = Event.objects.filter(date__gte=datetime.now()).order_by('date','start_time')
    context_object_name = 'upcoming_events'