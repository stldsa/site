from stl_dsa.users.views import UserUpdateView
from stl_dsa.users.models import User
from allauth.account.views import LoginView
from django.contrib.auth.models import Group

import pytest


@pytest.mark.django_db
def test_signup_view_post(client):
    response = client.post("/signup/", {"username": "a@abc.com", "password": "help123"})
    assert response.status_code == 200


def test_login_view_get(rf):
    request = rf.get("/login/")
    view = LoginView()
    view.setup(request)
    initial = view.get_initial()
    assert initial == {}


@pytest.mark.django_db
def test_login_view_post(client):
    response = client.post(
        "/login/", {"username": "admin@example.com", "password": "password"}
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_post_blank(client):
    response = client.post("/login/")
    assert response.status_code == 200


def test_update_routes_to_myDSA(rf, faker):
    first_name = faker.first_name()
    last_name = faker.last_name()
    request = rf.post(
        "/myDSA/update",
        data={
            "first_name": first_name,
            "last_name": last_name,
        },
    )
    request.user = User(first_name=first_name, last_name=last_name, email=faker.email())
    view = UserUpdateView()
    view.setup(request)

    assert view.get_success_url() == "/myDSA/"


def test_mydsa_unauthorized_redirect(client):
    response = client.get("/myDSA/")
    assert response.status_code == 302
    assert response.url == "/login/?next=/myDSA/"


def test_mydsa_authorized_as_member_success(client, django_user_model, mocker):
    user = django_user_model.objects.create_user(
        email="testuser@example.com", password="12345"
    )
    mocker.patch("stl_dsa.users.models.User.is_member", return_value=True)
    member = Group.objects.create(name="Members")
    user.groups.add(member)
    client.login(username="testuser@example.com", password="12345")
    response = client.get("/myDSA/")
    assert response.status_code == 200
