from datetime import datetime

import requests
from django.db import models
from wagtail.admin.panels import FieldPanel

from committees.models import CommitteePage


class APICalls(models.Model):
    datetime = models.DateTimeField(default=datetime.min)


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start = models.DateTimeField()
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip = models.IntegerField(null=True, blank=True)
    url = models.URLField()
    status = models.CharField(max_length=50, null=True, blank=True)
    host_formation = models.ForeignKey(
        CommitteePage, on_delete=models.SET_NULL, null=True, blank=True
    )
    uuid = models.UUIDField(null=True, blank=True)
    featured_image_url = models.URLField(null=True, blank=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("host_formation"),
    ]

    def __str__(self):
        return f"{str(self.start.date())} -- {self.title}"

    def fetch_embed_html(self):
        """Fetch widget embed HTML given the API endpoint for the event."""
        return requests.get("https://actionnetwork.org/oembed/?url=" + self.url).json()[
            "html"
        ]

    def transform_to_google_calendar(self):
        """Transform the Event object into a Google Calendar event object."""
        return {
            "summary": self.title,
            "description": self.description,
            "start": {
                "dateTime": self.start,
                "timeZone": "America/Chicago",
            },
            "end": {
                "dateTime": self.end_time,
                "timeZone": "America/Chicago",
            },
        }

    class Meta:
        ordering = ["-start"]
