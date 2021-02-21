# from django.http.response import HttpResponse
# import requests
# from django.contrib import auth
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
import json
from django.http import HttpResponse
from datetime import datetime


def list(request):
    events = [
        {
            "id": "event1",
            "title": "title1",
            "start": "2021-02-21",
        },
        {"id": "event2", "title": "title2"},
    ]
    return HttpResponse(json.dumps(events), content_type="application/json")


# class ListEvents(APIView):
#     # authentication_classes = [authentication.TokenAuthentication]

#     def get(self, request, format=None):
#         return Response()