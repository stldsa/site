import pytest


@pytest.fixture()
def events_api_response(client):
    return client.get("/api/events/")
