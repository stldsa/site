from stl_dsa.users.views import UserSignupView, UserUpdateView
from stl_dsa.users.tests.factories import UserFactory


def test_signup_view_from_homepage(rf):
    request = rf.get("/signup/")
    request.session = {"email": "test@example.com"}
    view = UserSignupView()
    view.setup(request)
    initial = view.get_initial()
    assert initial["email"] == "test@example.com"


def test_update_routes_to_myDSA(rf, db):
    user = UserFactory()
    request = rf.post(
        "/myDSA/update",
        data={
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    )
    request.user = user
    view = UserUpdateView()
    view.setup(request)

    assert view.get_success_url() == "/myDSA/"
