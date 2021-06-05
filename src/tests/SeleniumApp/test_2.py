import pytest
from django.test import LiveServerTestCase
from selenium import webdriver


@pytest.mark.skip
class BrowserTest(LiveServerTestCase):
    def test_headless(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(
            executable_path=r"./chromedriver",
            options=options
        )
        driver.get(f"{self.live_server_url}/admin/")
        assert "Log in | Django site admin" in driver.title
