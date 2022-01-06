from stl_dsa.users.models import User
import pytest
from django.contrib.auth.models import Group
from stl_dsa.users.tests.factories import UserFactory
from model_bakery import baker
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
def member_user(member_email):
    return baker.make("users.User", email=member_email)


@pytest.fixture
def nonmember_user(nonmember_email):
    return baker.make("users.User", email=nonmember_email)


@pytest.fixture
def member_person(db):
    person = baker.prepare("Person")
    person.id = 1
    person.tags.set("Voting Members")
    return person


@pytest.fixture
def member_uuid(faker):
    return faker.uuid4()


@pytest.fixture(scope="session")
def member_taggings_response():
    return [
        {
            "_links": {
                "osdi:tag": {
                    "href": "https://actionnetwork.org/api/v2/tags/7cb02320-3ecc-4479-898e-67769a1bf7be"
                }
            }
        }
    ]


# @pytest.fixture
# def user(nonmember_person):
#     user = UserFactory.build()
#     user.person = nonmember_person
#     return user


# @pytest.fixture
# def member(member_person):
#     user = UserFactory.build()
#     user.person = member_person
#     return user
