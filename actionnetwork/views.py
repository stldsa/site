from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
import requests


def person_helper(request):
    if request.method == "POST":
        data = {
            "person": {
                "postal_addresses": [{"postal_code": request.POST.get("zip")}],
                "email_addresses": [{"address": request.POST.get("email")}],
            }
        }
        print(data)
        response = requests.post(
            "https://actionnetwork.org/api/v2/people/",
            json=data,
            headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS["main"]},
        )
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            messages.success(request, "You've been added to our email list!")
    return HttpResponseRedirect("/")
