import pytest
from stl_dsa.users.views import UserUpdateView


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.add_argument("-headless")
    return firefox_options


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def member_update_response(rf, member):
    view = UserUpdateView()
    request = rf.get("/fake-url/")
    request.user = member
    view.request = request


@pytest.fixture
def test_password():
    return "strong-test-pass"
