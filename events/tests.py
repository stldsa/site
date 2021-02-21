from django.urls import reverse, resolve


def test_events_api_url_has_name():
    endpoint = reverse("events_api")
    assert endpoint == "/api/events/"


def test_events_api_url_routed(events_api_response):
    assert events_api_response.status_code == 200
    assert events_api_response["content-type"] == "application/json"


def test_events_api_url_resolves():
    resolver = resolve("/api/events/")
    assert resolver.view_name == "events_api"


# @pytest.mark.django_db
# def test_get_returns_event_list(events_api_response):
#     event_list = json.loads(events_api_response.content.decode("utf8"))
