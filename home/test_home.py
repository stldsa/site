from home.views import EmailFormView


def test_member_submits_email_and_is_redirected_to_login(rf, member):
    response = EmailFormView(email=member.email)

    assert response.get_success_url(emails=[member.email]) == "/login/"


def test_nonmember_submits_email_and_is_redirected_to_login(user):
    response = EmailFormView(email=user.email)
    assert response.get_success_url(emails=[]) == "/signup/"
