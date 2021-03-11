# from django.http.response import HttpResponse
# import requests
# from django.contrib import auth
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
import json
from django.http import HttpResponse
from action_network import get_events
from config.settings.local import ACTIONNETWORK_API_KEYS


def replace_id_key(event):
    event["id"] = event.pop("identifiers")
    event["start"] = event.pop("start_date")
    event["url"] = event.pop("browser_url")
    event = {
        key: value
        for key, value in event.items()
        if key in ["id", "title", "start", "url"]
    }
    return event


def list(request):
    all_events = []
    for api_key in ACTIONNETWORK_API_KEYS:
        events = get_events(api_key)
        events = [replace_id_key(event) for event in events]
        all_events += events
    return HttpResponse(json.dumps(all_events), content_type="application/json")


# class ListEvents(APIView):
#     # authentication_classes = [authentication.TokenAuthentication]

#     def get(self, request, format=None):
#         return Response()