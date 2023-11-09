import pytest
import responses


@pytest.fixture(scope="session")
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def member_email():
    return "member@example.com"


@pytest.fixture
def nonmember_email():
    return "nonmember@example.com"


@pytest.fixture
def member_uuid(faker):
    return faker.uuid4()


@pytest.fixture(scope="session")
def member_taggings_response():
    return [
        {
            "_links": {
                "osdi:tag": {
                    "href": (
                        "https://actionnetwork.org/api/v2/tags/"
                        "7cb02320-3ecc-4479-898e-67769a1bf7be"
                    )
                }
            }
        }
    ]
