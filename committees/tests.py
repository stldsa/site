import pytest
from stl_dsa.users.tests.factories import UserFactory
from committees.models import Person
from model_bakery import baker
from faker import Faker

fake = Faker()


@pytest.mark.django_db
def test_person_email_matches_user_email():
    user = UserFactory()
    assert user.person.email == user.email


def test_get_action_network_id():
    person = baker.prepare("Person", id=baker.seq(1))
    id = fake.uuid4()

    people = [
        {
            "email_addresses": [{"address": person.email}],
            "identifiers": ["action_network:" + id],
        }
    ]

    assert person.uuid(people=people) == id
