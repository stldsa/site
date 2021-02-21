import requests
import os
import json


def get_events(key):
    events_response = requests.get(
        "https://actionnetwork.org/api/v2/events/",
        # params={"filter": f"modified_date gt '{last_api_call}'"},
        headers={"OSDI-API-Token": key},
    )
    events_json = events_response.json()
    return events_json["_embedded"]["osdi:events"]
