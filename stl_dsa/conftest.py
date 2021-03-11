import pytest
from django.test import RequestFactory

from stl_dsa.users.models import User
from stl_dsa.users.tests.factories import UserFactory


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.add_argument("-headless")
    return firefox_options


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()
