from stl_dsa.users.views import UserSignupView


def test_signup_view_from_homepage(rf):
    request = rf.get("/signup/")
    request.session = {"email": "test@example.com"}
    view = UserSignupView()
    view.setup(request)
    initial = view.get_initial()
    assert initial["email"] == "test@example.com"
