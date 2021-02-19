def test_new_visitor(selenium):
    # Visitor visits the login page
    selenium.get("http://localhost:8000/accounts/login/")
