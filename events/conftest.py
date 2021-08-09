import pytest
from events.api import views


@pytest.fixture(scope="module")
def vcr_config(vcr_config):
    return {
        "filter_headers": [("OSDI-API-Token", "abcdefghijklmnopqrstuvwxyz123456")],
    }
