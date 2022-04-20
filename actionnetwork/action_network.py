import requests
import logging
from django.conf import settings
from urllib.parse import urljoin
from django.apps import apps

API_URL = "https://actionnetwork.org/api/v2"
people_URL = urljoin(API_URL, "people")
logger = logging.getLogger("action_network")


class Resource:
    def __init__(self, name, group="main", uuid=None, href=None, resource=None):
        self.name = name
        self.group = group
        self.uuid = uuid
        self.href = href
        self.resource = resource or name

    def get_group_api_key(group):
        return settings.ACTIONNETWORK_API_KEYS[group]

    def get_response(href, api_key):
        response = requests.get(
            href,
            headers={"OSDI-API-Token": api_key},
        )
        if response.ok:
            return response
        logger.error("get_response error!", response.json)
        return None


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


def call_api(URI, params=None, group="main"):
    response = requests.get(
        URI,
        params=params,
        headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS[group]},
    )
    if response.ok:
        return response.json()
    logger.error(f"call_api error! for URI={URI}", response.json)
    return None


class People:
    def __init__(self, json: str):
        self.json = json

    URI = people_URL

    @classmethod
    def from_email(cls, email):
        people = call_api(people_URL, {"filter": f"email_address eq '{email}'"})
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
        return urljoin(people_URL, f"{self.person_uuid}/taggings")

    @property
    def json(self):
        return call_api(self.URI)

    def get_taggings(self):
        return call_api(self.URI)

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
    def __init__(self, json):
        self.json = json

    @classmethod
    def from_uuid(cls, uuid):
        uri = urljoin(cls.people_endpoint, uuid)
        return cls(call_api(uri))

    @classmethod
    def from_people(cls, people: People):
        person_list = people.json["_links"]["osdi:people"]
        if first_person := next(iter(person_list), None):
            return cls(call_api(first_person["href"]))

    @classmethod
    def from_URI(cls, URI):
        return cls(call_api(URI))

    @property
    def URI(self):
        return self.people_endpoint + self.uuid

    @property
    def uuid(self):
        return [
            id.split(":")[1]
            for id in self.json.get("identifiers", [])
            if id.split(":")[0] == "action_network"
        ][0]

    @property
    def taggings(self):
        return Taggings(self.uuid)
