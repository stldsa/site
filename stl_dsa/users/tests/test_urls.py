from django.urls import reverse, resolve


def test_detail():
    assert reverse("users:detail") == "/myDSA/"
    assert resolve("/myDSA/").view_name == "users:detail"


def test_update():
    assert reverse("users:update") == "/myDSA/update/"
    assert resolve("/myDSA/update/").view_name == "users:update"


def test_login():
    assert reverse("account_login") == "/login/"
    assert resolve("/login/").view_name == "account_login"


def test_signup():
    assert reverse("account_signup") == "/signup/"
    assert resolve("/signup/").view_name == "account_signup"
