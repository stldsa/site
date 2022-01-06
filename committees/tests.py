import pytest
from actionnetwork import action_network as an
from stl_dsa.users.tests.factories import UserFactory
from faker import Faker
from django.contrib.auth.models import Group
from model_bakery import baker
import responses

fake = Faker()


@pytest.mark.django_db
def test_person_email_matches_user_email():
    user = UserFactory()
    assert user.person.email == user.email


def test_get_action_network_id(faker):
    person_json = {
        "email_addresses": [{"address": faker.email()}],
        "identifiers": ["action_network:" + faker.uuid4()],
    }
    assert an.identifiers_to_dicts(person_json["identifiers"])["action_network"]


@pytest.mark.django_db
def test_update_membership(mocked_responses, member_uuid, member_taggings_response):
    person = baker.make("users.User").person
    person.uuid = member_uuid
    mocked_responses.add(
        responses.GET,
        an.AN_API_URL + "/people/" + person.uuid + "/taggings",
        json=member_taggings_response,
    )
    member_group = Group.objects.create(name="Members")
    person.update_membership()

    assert member_group in person.user.groups.all()
