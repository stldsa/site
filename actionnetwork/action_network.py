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


def get_events():
    return [
        Resource("events", group).list
        for group in settings.ACTIONNETWORK_API_KEYS.keys()
    ]


def save_event(event):
    apps.get_model("events", "Event").objects.update_or_create(
        id=event["identifiers"][0].split(":")[1],
        defaults={
            "title": event["title"],
            "start": event["start_date"],
            "url": event["browser_url"],
            "description": event["description"],
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
            data = call_api("people", params=params).json()
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

    URI = people_URL

    @classmethod
    def from_email(cls, email):
        people = call_api(
            people_URL, params={"filter": f"email_address eq '{email}'"}
        ).json()
        return cls(people)

    @property
    def list(self):
        if self.json is None:
            logger.error("error with People.list!", self)
            return None
        return self.json["_embedded"]["osdi:people"]


class Taggings:
    def __init__(self, person_uuid):
        self.person_uuid = person_uuid

    @property
    def URI(self):
        return f"people/{self.person_uuid}/taggings"

    def get_taggings(self):
        return call_api(self.URI).json()

    @property
    def tags(self):
        return [
            tagging["href"]
            for tagging in self.get_taggings()["_links"]["osdi:taggings"]
        ]

    def has_tag(self, tag_id):
        return any(tag_id in tag for tag in self.tags)


class Tags:
    pass


class Tag:
    def __init__(self, json):
        self.json = json

    @classmethod
    def from_uuid(cls, uuid):
        uri = f"{API_URL}/tags/{uuid}"
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

    # @property
    # def uuid(self):
    #     return [
    #         id.split(":")[1]
    #         for id in self.json.get("identifiers", [])
    #         if id.split(":")[0] == "action_network"
    #     ][0]

    @property
    def taggings(self):
        return Taggings(self.uuid)
