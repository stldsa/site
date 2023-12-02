import logging
from urllib.parse import urljoin

import requests
from django.apps import apps
from django.conf import settings

API_URL = "https://actionnetwork.org/api/v2/"
people_URL = urljoin(API_URL, "people")
logger = logging.getLogger("action_network")


class Resource:
    def __init__(self, name, group="main", uuid=None, href=None, resource=None):
        self.name = name
        self.group = group
        self.uuid = uuid
        self.href = href
        self.resource = resource or name

    def get_group_api_key(self, group):
        return settings.ACTIONNETWORK_API_KEYS[group]

    def get_response(self, href, api_key):
        return requests.get(
            href,
            headers={"OSDI-API-Token": api_key},
        )


class Events:
    def __init__(self, group):
        self.group = group

    def get(self):
        return call_api("events", group=self.group).json()["_embedded"]["osdi:events"]


def save_event(event):
    apps.get_model("events", "Event").objects.update_or_create(
        uuid=event["identifiers"][0].split(":")[1],
        defaults={
            "title": event["title"],
            "start": event["start_date"][:-1],
            "url": event["browser_url"],
            "description": event["description"],
            "status": event["status"],
            "featured_image_url": event.get("featured_image_url"),
        },
    )


def call_api(resource, params=None, group="main"):
    URI = urljoin(API_URL, resource)
    response = requests.get(
        URI,
        params=params,
        headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS[group]},
    )
    return response


class People:
    def __init__(self, data=None, email=None):
        params = {"filter": f"email_address eq '{email}'"} if email else None
        if data is None:
            data = call_api(self.name, params=params).json()
        if links := data.get("_links"):
            self.ids = [
                person["href"].split("/")[-1] for person in links["osdi:people"]
            ]
        else:
            self.ids = []
        if embedded := data.get("_embedded"):
            self.people = embedded["osdi:people"]
        else:
            self.people = []

    name = "people"

    @classmethod
    def from_email(cls, email):
        data = call_api(
            cls.name, params={"filter": f"email_address eq '{email}'"}
        ).json()
        return cls(data)


class Taggings:
    def __init__(self, person_uuid):
        self.person_uuid = person_uuid
        self.data = call_api(self.resource).json()

    @property
    def resource(self):
        return f"people/{self.person_uuid}/taggings"

    @property
    def tags(self):
        if embedded := self.data.get("_embedded"):
            taggings = embedded.get("osdi:taggings")
        else:
            taggings = []
        hrefs = [tagging["_links"]["osdi:tag"]["href"] for tagging in taggings]
        return [href.split("/")[-1] for href in hrefs]


class Tags:
    def __init__(self, data=None):
        if data is None:
            self.data = call_api("tags").json()
        self.tags = self.data["_embedded"]["OSDI:tags"]
        self.names = [tag["name"] for tag in self.tags]

    def find_tag_id(self, tag_name):
        return [[tag["id"] for tag in self.tags if tag["name"] == "Voting Member"]][0]


class Tag:
    def __init__(self, json):
        self.json = json

    @classmethod
    def from_uuid(cls, uuid):
        uri = f"tags/{uuid}"
        return cls(call_api(uri))


class Person:
    def __init__(self, uuid):
        self.uuid = uuid

    @property
    def json(self):
        return requests.get(
            f"https://actionnetwork.org/api/v2/people/{self.uuid}",
            headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS["main"]},
        ).json()

    @classmethod
    def first_from_people(cls, people: People):
        return people.people[0] if people.people else None

    @classmethod
    def from_URI(cls, URI):
        return cls(call_api(URI))

    @property
    def taggings(self):
        return Taggings(self.uuid)

    @property
    def custom_fields(self):
        return self.json.get("custom_fields")
