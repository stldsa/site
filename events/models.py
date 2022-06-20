from datetime import datetime
from django.db import models
from committees.models import CommitteePage
from wagtailmenus.models import AbstractLinkPage


class APICalls(models.Model):
    datetime = models.DateTimeField(default=datetime.min)


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start = models.DateTimeField()
    end_time = models.TimeField(null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip = models.IntegerField(null=True, blank=True)
    formation = models.ForeignKey(
        CommitteePage,
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        related_name="events",
    )
    url = models.URLField()
    status = models.CharField(max_length=50, null=True, blank=True)
    id = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.title + " " + str(self.start)


class EventsPage(AbstractLinkPage):
    pass
