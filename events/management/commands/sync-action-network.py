from actionnetwork import action_network as an
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for group in settings.ACTIONNETWORK_API_KEYS.keys():
            events = an.Events(group=group).list
            for event in events:
                an.save_event(event)
