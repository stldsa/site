from stl_dsa.users.views import UserSignupView
from home.views import EmailFormView


def test_user_submits_email_and_is_redirected_to_login(rf, faker):
    email = faker.email()
    request = rf.post("/", {"email": email})
    view = EmailFormView()
    view.setup(request)

    assert view.get_success_url(emails=[email]) == "/login/"


def test_nonuser_submits_email_and_is_redirected_to_login(rf, faker):
    request = rf.post("/", {"email": faker.email()})
    view = EmailFormView()
    view.setup(request)
    assert view.get_success_url(emails=["test@example.com"]) == "/signup/"


def test_form_submit_sets_session_data(rf, faker):
    email = faker.email()
    request = rf.get("/signup/")
    request.session = {"email": email}
    view = UserSignupView()
    view.setup(request)
    assert view.get_initial().get("email") == email
