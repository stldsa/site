import pytest
from events.api import views


@pytest.fixture()
def events_api_response(rf):
    request = rf.get("/api/events/")
    return views.list(request)