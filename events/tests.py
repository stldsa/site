from django.urls import resolve, reverse


def test_events_api_url_routed():

    assert reverse("users:detail") == "/myDSA/"
    assert resolve("/myDSA/").view_name == "users:detail"


def test_events_api_url_resolves():
    resolver = resolve("/api/events/")
    assert resolver.view_name == "event-list"
