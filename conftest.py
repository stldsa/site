import pytest
from stl_dsa.users.tests.factories import UserFactory
from model_bakery import baker


@pytest.fixture
def nonuser():
    return baker.prepare("Person")


@pytest.fixture
def nonmember_person():
    person = baker.prepare("Person")
    person.tags = []
    return person


@pytest.fixture
def member_person():
    person = baker.prepare("Person")
    person.tags = ["Voting Members"]
    return person


@pytest.fixture
def user(nonmember_person):
    user = UserFactory.build()
    user.person = nonmember_person
    return user


@pytest.fixture
def member(member_person):
    user = UserFactory.build()
    user.person = member_person
    return user
