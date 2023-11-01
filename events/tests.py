from django.urls import resolve, reverse

from events.models import Event


def test_events_api_url_routed():
    assert reverse("users:detail") == "/myDSA/"
    assert resolve("/myDSA/").view_name == "users:detail"


def test_events_api_url_resolves():
    resolver = resolve("/api/events/")
    assert resolver.view_name == "event-list"


def test_post_event_to_google_calendar():
    google_event = {
        "summary": "Workplace Organizing Training Series Part 2",
        "description": "Trinity has accessible entrances",
        "start": {
            "dateTime": "2023-11-02T18:30:00-05:00",
            "timeZone": "America/Chicago",
        },
        "end": {
            "dateTime": "2023-11-02T20:30:00-05:00",
            "timeZone": "America/Chicago",
        },
    }
    db_event = Event(
        start="2023-11-02T18:30:00-05:00",
        end_time="2023-11-02T20:30:00-05:00",
        title="Workplace Organizing Training Series Part 2",
        description="Trinity has accessible entrances",
    )
    assert db_event.transform_to_google_calendar() == google_event
