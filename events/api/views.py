# from django.http.response import HttpResponse
# import requests
# from django.contrib import auth
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
import json
from django.http import HttpResponse
from action_network import get_events


def replace_id_key(event):
    event["id"] = event.pop("identifiers")
    return event


def list(request):
    events = get_events()
    events = [replace_id_key(event) for event in events]
    return HttpResponse(json.dumps(events), content_type="application/json")


# class ListEvents(APIView):
#     # authentication_classes = [authentication.TokenAuthentication]

#     def get(self, request, format=None):
#         return Response()