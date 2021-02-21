import requests
import os
import json


def get_events():
    events_response = requests.get(
        "https://actionnetwork.org/api/v2/events/",
        # params={"filter": f"modified_date gt '{last_api_call}'"},
        headers={"OSDI-API-Token": os.getenv("AN_API_KEY")},
    )
    events_json = json.loads(events_response.content)
    return events_json["_embedded"]["osdi:events"]
