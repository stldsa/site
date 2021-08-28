import pytest
from stl_dsa.users.tests.factories import UserFactory


@pytest.fixture
def user():
    return UserFactory.build()


@pytest.fixture
def member():
    return UserFactory.build(groups={"member"})
