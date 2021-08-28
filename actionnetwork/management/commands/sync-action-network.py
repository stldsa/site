from actionnetwork import action_network as an
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        events = an.get_events()
        for event in events:
            an.save_events(event)
