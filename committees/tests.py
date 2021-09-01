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


@pytest.mark.django_db
def test_person_is_member():
    member_person = baker.make("Person")
    member_person.tags.add("Voting Members")
    # nonmember_person = baker.make("Person")
    assert member_person.is_member
    # assert not nonmember_person.is_member
