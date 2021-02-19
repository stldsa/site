import pytest
from stl_dsa.users.models import User
from stl_dsa.users.views import UserRedirectView, UserUpdateView

pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(self, user: User, rf):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.id}/"

    def test_get_object(self, user: User, rf):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user

    @pytest.mark.django_db
    def test_user_membership(self, client, user):
        pass


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf):
        view = UserRedirectView()
        request = rf.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.id}/"
