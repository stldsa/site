from datetime import datetime
from django.db import models
from wagtail.models import Page
from wagtailmenus.models import AbstractLinkPage
from wagtail.admin.panels import FieldPanel

from committees.models import CommitteePage


class APICalls(models.Model):
    datetime = models.DateTimeField(default=datetime.min)


class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    uuid = models.UUIDField(null=True)
    host_formation = models.ForeignKey(
        CommitteePage, on_delete=models.SET_NULL, null=True, blank=True
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("host_formation"),
    ]

    def __str__(self):
        return f"{self.title} {str(self.start.date())}"

    class Meta:
        ordering = ["-start"]


class EventsPage(AbstractLinkPage):
    search_fields = Page.search_fields
