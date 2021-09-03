import requests
from django.conf import settings
from urllib.parse import urlparse
import pathlib
from django.apps import apps


class Resource:
    def __init__(self, name, group="main", uuid=None, href=None, resource=None):
        self.name = name
        self.group = group
        self.uuid = uuid
        self.href = href
        self.resource = resource or name

    @property
    def json(self):
        return requests.get(
            self.href
            or "/".join(
                filter(
                    None,
                    ("https://actionnetwork.org/api/v2/", self.name, self.uuid),
                )
            ),
            headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS[self.group]},
        ).json()

    @property
    def list(self):
        json = self.json
        print(json)
        return json["_embedded"].get(f"osdi:{self.resource}", [])


def get_events():
    return {
        group: Resource("events", group).list
        for group in settings.ACTIONNETWORK_API_KEYS.keys()
    }


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


def get_tag(tag_name, tag_list):
    return next(
        (tag_json for tag_json in tag_list if tag_json["name"] == tag_name), None
    )


def get_resource_href(resource_json, href_name):
    return resource_json[f"osdi:{href_name}"]["href"]


def get_resources_hrefs(resource_list, href_name):
    return [get_resource_href(resource, href_name) for resource in resource_list]


def get_emails_given_emails_json(emails_json):
    return [email["address"] for email in emails_json]


def get_emails_from_people_resources(resources):
    email_addresses = [resource["email_addresses"] for resource in resources]
    return [
        email["address"] for person_emails in email_addresses for email in person_emails
    ]


def id_str_to_key_value(id_str):
    return id_str.split(":")


def identifiers_to_dicts(identifiers):
    return dict(id_str_to_key_value(identifier) for identifier in identifiers)


def get_person_id_from_people_given_email(email, people):
    return next(
        (
            identifiers_to_dicts(person["identifiers"])["action_network"]
            for person in people
            if email in get_emails_given_emails_json(person["email_addresses"])
        ),
        None,
    )


def get_href_from_id(id_str):
    return f"https://actionnetwork.org/api/v2/{id_str}/"


def get_id_from_href(href):
    print(href)

    return pathlib.Path(urlparse(href).path).stem


def get_tag_href_from_tagging(tagging):
    return tagging["_links"]["osdi:tag"]["href"]
