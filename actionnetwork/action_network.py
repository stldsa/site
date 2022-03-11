import requests
import logging
from django.conf import settings
from urllib.parse import urljoin
from django.apps import apps

API_URL = "https://actionnetwork.org/api/v2"
People_URL = urljoin(API_URL, "people")

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
        else:
            logger.error("get_response error!", response.json)
            return None

    @property
    def list(self):
        return self.json["_embedded"]["osdi:people"]


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
    else:
        logger.error("call_api error! for URI=" + URI, response.json)
        return None


class Events:
    def __init__(self, json=None, group="main"):
        self.json = json or call_api(
            "https://actionnetwork.org/api/v2/events", group=group
        )

    @property
    def list(self):
        return self.json["_embedded"]["osdi:events"]


class People:
    def __init__(self, json):
        self.json = json

    URI = People_URL

    @classmethod
    def from_email(cls, email):
        get_email_URL = People_URL + f"?filter=email_address eq '{email}'"
        people = call_api(get_email_URL)
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
        return urljoin(People_URL, self.person_uuid + "/taggings")

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
        uri = API_URL + "/tags/" + uuid
        return cls(call_api(uri))


class Person:
    def __init__(self, json):
        self.json = json

    @classmethod
    def from_uuid(cls, uuid):
        uri = urljoin(cls.people_endpoint, uuid)
        return cls(call_api(uri))

    @classmethod
    def from_people(cls, people):
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
        if id := next(iter(self.json.get("identifiers", [])), ""):
            return id.split(":")[1]
        else:
            return None

    @property
    def taggings(self):
        return Taggings(self.uuid)
