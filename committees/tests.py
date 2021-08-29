from committees.models import Person
from faker import Faker

fake = Faker()


def test_get_email(user):
    assert Person(user=user, email=user.email).email == user.email
    assert user.person.email == user.email


def test_get_action_network_id():
    email = fake.email()
    person = Person(email=email)
    id = fake.uuid4()

    people = [
        {
            "email_addresses": [{"address": email}],
            "identifiers": ["action_network:" + id],
        }
    ]

    assert person.action_network_id(people=people) == id


def test_person_is_member():
    member = Person()
    nonmember = Person()
    member.tags = ["Voting Members"]
    nonmember.tags = []

    assert member.is_member
    assert not nonmember.is_member
