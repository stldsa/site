from stl_dsa.users.views import UserSignupView, UserUpdateView
from stl_dsa.users.models import User


def test_signup_view_from_homepage(rf):
    request = rf.get("/signup/")
    request.session = {"email": "test@example.com"}
    view = UserSignupView()
    view.setup(request)
    initial = view.get_initial()
    assert initial["email"] == "test@example.com"


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
