import pytest
from django.test import LiveServerTestCase


@pytest.mark.skip
@pytest.mark.usefixtures("chrome_driver_init")
class BrowserTest(LiveServerTestCase):
    def test_admin_page(self):
        # the driver we access using self is headless already
        # conftest.py file run before any test hence update the 
        # driver attribute of class 
        self.driver.get(f"{self.live_server_url}/admin/")
        assert "Log in | Django site admin" in self.driver.title
