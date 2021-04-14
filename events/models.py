import requests
from datetime import datetime
from django.db import models
from committees.models import Committee, CommitteePage

# Create your models here.


class APICalls(models.Model):
    datetime = models.DateTimeField(default=datetime(1, 1, 1, 1, 1, 1))


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    start = models.DateTimeField()
    end_time = models.TimeField(null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip = models.IntegerField(null=True, blank=True)
    formation = models.ForeignKey(
        Committee, null=True, on_delete=models.CASCADE, blank=True
    )
    actionnetwork_url = models.URLField()
    actionnetwork_id = models.CharField(max_length=50)

    def __str__(self):
        return self.title + " " + str(self.date)
