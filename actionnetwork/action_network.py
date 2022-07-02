import requests
import logging
from django.conf import settings
from urllib.parse import urljoin
from django.apps import apps

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
        response = requests.get(
            href,
            headers={"OSDI-API-Token": api_key},
        )
        return response


class Events:
    def __init__(self, group):
        self.group = group

    def get(self):
        return call_api("events", group=self.group).json()["_embedded"]["osdi:events"]


def save_event(event):
    apps.get_model("events", "Event").objects.update_or_create(
        id=event["identifiers"][0].split(":")[1],
        defaults={
            "title": event["title"],
            "start": event["start_date"],
            "url": event["browser_url"],
            "description": event["description"],
            "status": event["status"],
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

    @property
    def list(self):
        if self.json is None:
            logger.error("error with People.list!", self)
            return None
        return self.json["_embedded"]["osdi:people"]


class Taggings:
    def __init__(self, person_uuid):
        self.person_uuid = person_uuid
        self.data = call_api(self.resource).json()

    @property
    def resource(self):
        return f"people/{self.person_uuid}/taggings"

    @property
    def tags(self):
        taggings = self.data["_embedded"]["osdi:taggings"]
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
    def __init__(self, data):
        self.uuid = [
            id.split(":")[1]
            for id in data.get("identifiers", [])
            if id.split(":")[0] == "action_network"
        ][0]

    @classmethod
    def from_uuid(cls, uuid):
        uri = urljoin(cls.people_endpoint, uuid)
        return cls(call_api(uri))

    @classmethod
    def first_from_people(cls, people: People):
        return people.people[0] if people.people else None

    @classmethod
    def from_URI(cls, URI):
        return cls(call_api(URI))

    @property
    def URI(self):
        return self.people_endpoint + self.uuid

    @property
    def taggings(self):
        return Taggings(self.uuid)
