import pytest
from django.urls import reverse, resolve

from stl_dsa.users.models import User

pytestmark = pytest.mark.django_db


def test_detail(user: User):
    assert reverse("users:detail", kwargs={"id": user.id}) == f"/users/{user.id}/"
    assert resolve(f"/users/{user.id}/").view_name == "users:detail"


def test_update():
    assert reverse("users:update") == "/users/~update/"
    assert resolve("/users/~update/").view_name == "users:update"


def test_redirect():
    assert reverse("users:redirect") == "/users/~redirect/"
    assert resolve("/users/~redirect/").view_name == "users:redirect"
