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


def test_nonuser_submits_without_email_and_is_redirected_to_signup(rf, faker):
    request = rf.post("/", {"email": ""})
    view = EmailFormView()
    view.setup(request)
    assert view.get_success_url(emails=["test@example.com"]) == "/signup/"
