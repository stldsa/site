import requests
import action_network as an
from django.core.management.base import BaseCommand
from events.models import Event


class Command(BaseCommand):
    def handle(self, *args, **options):
        event_list = an.get_events()
        for events in event_list:
            an.save_events(events)
