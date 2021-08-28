from django.urls import resolve, reverse


def test_events_api_url_routed():

    assert reverse("users:detail") == "/myDSA/"
    assert resolve("/myDSA/").view_name == "users:detail"


def test_events_api_url_resolves():
    resolver = resolve("/api/events/")
    assert resolver.view_name == "event-list"


# def test_get_returns_event_list(db, client):
#     events_api_response = client.get("/api/events/")
#     event_list = json.loads(events_api_response.content.decode("utf8"))
#     assert all(
#         [{"id", "title", "start", "url"} == event.keys() for event in event_list]
#     )
