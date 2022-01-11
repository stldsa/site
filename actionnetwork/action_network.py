import requests
from django.conf import settings
from urllib.parse import urljoin
from django.apps import apps

API_URL = "https://actionnetwork.org/api/v2"


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
        return requests.get(
            href,
            headers={"OSDI-API-Token": api_key},
        )


def get_events():
    return [
        Resource("events", group).list
        for group in settings.ACTIONNETWORK_API_KEYS.keys()
    ]


def save_events(events):
    for event in events:
        apps.get_model("events", "Event").objects.update_or_create(
            id=event["identifiers"][0].split(":")[1],
            defaults={
                "title": event["title"],
                "start": event["start_date"],
                "url": event["browser_url"],
                "description": event["description"],
            },
        )


def call_api(URI, params=None):
    return requests.get(
        URI,
        params=params,
        headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS["main"]},
    ).json()


class People:
    def __init__(self, json):
        self.json = json

    URI = urljoin(API_URL, "people")

    @classmethod
    def from_email(cls, email):
        people = call_api(
            f"https://actionnetwork.org/api/v2/people?filter=email_address eq '{email}'"
        )
        return cls(people)

    @property
    def list(self):
        return self.json["_embedded"]["osdi:people"]


class Taggings:
    def __init__(self, person_uuid):
        self.person_uuid = person_uuid

    @property
    def URI(self):
        return API_URL + "/people/" + self.person_uuid + "/taggings"

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
        first_person = next(iter(person_list), None)
        if first_person:
            return cls(call_api(first_person["href"]))

    @classmethod
    def from_URI(cls, URI):
        return cls(call_api(URI))

    @property
    def URI(self):
        return self.people_endpoint + self.uuid

    @property
    def uuid(self):
        id = next(iter(self.json.get("identifiers", [])), "")
        if id:
            return id.split(":")[1]
        else:
            return None

    @property
    def taggings(self):
        return Taggings(self.uuid)
