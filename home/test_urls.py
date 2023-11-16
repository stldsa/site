from django.test import TestCase
from django.urls import reverse


class TestUrls(TestCase):
    urls = [
        "/",
        "/about/",
        "/formations/",
        "/login/",
        "/updates/",
        "/join/",
        "/signup/",
    ]

    def test_urls(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_user_login_workflow(self):
        # Test login page
        login_url = reverse("account_login")
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)

        # Test login with correct credentials
        response = self.client.post(
            login_url, {"username": "admin@example.com", "password": "stldsa"}
        )
        self.assertRedirects(response, reverse("users:detail"))

        # Test login with incorrect credentials
        response = self.client.post(
            login_url, {"username": "testuser", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertContains(response, "Please enter a correct username and password.")
