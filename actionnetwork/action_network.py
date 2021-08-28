import requests
from django.conf import settings
from events.models import Event


def get_resource(resource, group):
    return requests.get(
        "https://actionnetwork.org/api/v2/" + resource + "/",
        headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS[group]},
    )


def get_resource_list(resource, group):
    response = get_resource(resource, group)
    return response.json()["_embedded"][f"osdi:{resource}"]


def get_events():
    def get_events_for_formation(formation):
        events_response = get_resource("events", formation)
        events_json = events_response.json()
        return events_json["_embedded"]["osdi:events"]

    return [
        get_events_for_formation(key) for key in settings.ACTIONNETWORK_API_KEYS.keys()
    ]


def save_events(events):
    for event in events:
        Event.objects.update_or_create(
            id=event["identifiers"][0].split(":")[1],
            defaults={
                "title": event["title"],
                "start": event["start_date"],
                "url": event["browser_url"],
                "description": event["description"],
            },
        )


def get_emails():
    messages_response = requests.get(
        "https://actionnetwork.org/api/v2/messages/",
        headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS["main"]},
    )
    events_json = messages_response.json()
    return events_json["_embedded"]["osdi:messages"]


def get_tags():
    return get_resource("tags", "main")


<<<<<<< HEAD
def get_tag_taggings_href(tag):
    tags = get_resource_list("tags", "main")
    return next(item for item in tags if item["name"] == tag)["_links"][
        "osdi:taggings"
    ]["href"]
=======
# def get_tag(tag):
#     tags_response = requests.get("https://actionnetwork.org/api/v2/tags/",
#     headers=
#     )
def tag_list():
    pass
>>>>>>> main
