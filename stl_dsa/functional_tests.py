from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_home_page(self):
        self.browser.get("http://localhost:8000")
        assert "St Louis DSA" in self.browser.title