import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime

import requests
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

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

    def post_to_gcal(self):
        """Post event to Google Calendar."""
        scopes = ["https://www.googleapis.com/auth/calendar"]
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secret.json", scopes
                )
                creds = flow.run_local_server(port=0, open_browser=False)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        with build("calendar", "v3", credentials=creds) as gcal:
            print(gcal.calendarList().list().execute())
            gcal.events().insert(
                calendarId="admin@stldsa.org",
                body={
                    "summary": self.title,
                    "description": self.description,
                    "start": {
                        "dateTime": self.start.isoformat(),
                        "timeZone": "America/Chicago",
                    },
                    "end": {
                        "dateTime": self.start.isoformat(),
                        "timeZone": "America/New_York",
                    },
                },
            ).execute()

    class Meta:
        ordering = ["-start"]


class EventPage(Page):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    needs_childcare = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    content_panels = Page.content_panels + [
        FieldPanel("needs_childcare"),
        FieldPanel("is_public"),
    ]
