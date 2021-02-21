import pytest
from django.urls import reverse, resolve


@pytest.mark.django_db
def test_events_api_url_routed(client):
    endpoint = reverse("events_api")
    assert endpoint == "/api/events/"
    response = client.get(endpoint)
    assert response.status_code == 200
    assert response["content-type"] == "application/json"


@pytest.mark.django_db
def test_events_api_url_resolves():
    resolver = resolve("/api/events/")
    assert resolver.view_name == "events_api"


@pytest.mark.django_db
def test_get_returns_event_list(client):
    assert json.loads(response.content.decode("utf8"))
