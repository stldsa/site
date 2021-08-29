from committees.models import Person
from model_bakery import baker
from faker import Faker

fake = Faker()


def test_get_email(user):
    assert Person(user=user, email=user.email).email == user.email
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


def test_person_is_member(member_person, nonmember_person):
    assert member_person.is_member
    assert not nonmember_person.is_member
