# from django.http.response import HttpResponse
# import requests
# from django.contrib import auth
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
from django.http import HttpResponse


def list(request):
    return HttpResponse(content_type="application/json")


# class ListEvents(APIView):
#     # authentication_classes = [authentication.TokenAuthentication]

#     def get(self, request, format=None):
#         return Response()