from django_ical.views import ICalFeed
from events.models import Event


class EventFeed(ICalFeed):
    """
    A simple event calender
    """

    timezone = "America/Chicago"
    file_name = "stldsa.ics"

    def items(self):
        return Event.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        return item.start

    def item_link(self, item):
        return item.url
