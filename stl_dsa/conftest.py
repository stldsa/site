from django.contrib.auth.models import Group
import pytest

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
def member_group(db) -> Group:
    member_group, _ = Group.objects.get_or_create(name="Member")
    return member_group


@pytest.fixture
def member(user, member_group):
    user.groups.add(member_group)
    return user


@pytest.fixture
def member_update_response(member):
    view = UserUpdateView()
    request = rf.get("/fake-url/")
    request.user = user
    view.request = request


@pytest.fixture
def test_password():
    return "strong-test-pass"
