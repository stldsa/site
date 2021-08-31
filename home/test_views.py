from stl_dsa.users.views import UserSignupView
from home.views import EmailFormView


def test_member_submits_email_and_is_redirected_to_login(rf, member):
    request = rf.post("/", {"email": member.email})
    view = EmailFormView()
    view.setup(request)

    assert view.get_success_url(emails=[member.email]) == "/login/"


def test_nonmember_submits_email_and_is_redirected_to_login(rf, user):
    request = rf.post("/", {"email": user.email})
    view = EmailFormView()
    view.setup(request)
    assert view.get_success_url() == "/signup/"


def test_form_submit_sets_session_data(rf, user):
    request = rf.get("/signup/")
    request.session = {"email": user.email}
    view = UserSignupView()
    view.setup(request)
    assert view.get_initial().get("email") == user.email
