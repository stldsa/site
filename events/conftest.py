import pytest
from events.api import views


@pytest.fixture()
def events_api_response(rf):
    request = rf.get("/api/events/")
    return views.list(request)


@pytest.fixture(scope="module")
def vcr_config(vcr_config):
    return {
        "filter_headers": [("OSDI-API-Token", "abcdefghijklmnopqrstuvwxyz123456")],
    }
