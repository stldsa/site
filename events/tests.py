import pytest
from django.urls import reverse, resolve


# @pytest.mark.firefox_arguments("-headless")
# def test_full_calendar(selenium, live_server):
#     selenium.get(live_server + "/fullcalendar")


@pytest.mark.django_db
def test_fullcalendar_template_used(client):
    response = client.get("/fullcalendar/")
    assert response.status_code == 200
    assert "fullcalendar.html" in [template.name for template in response.templates]


@pytest.mark.django_db
def test_events_api_url_named(client):
    endpoint = reverse("events_api")
    assert endpoint == "/api/events/"
    response = client.get(endpoint)
    assert response.status_code == 200
    assert response["content-type"] == "application/json"


@pytest.mark.django_db
def test_events_api_url_resolves():
    resolver = resolve("/api/events/")
    assert resolver.view_name == "events_api"
