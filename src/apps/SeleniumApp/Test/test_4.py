import pytest


@pytest.mark.usefixtures("driver_init")
class TestAdminPage:
    # instead of live_server_url from django test class we use
    # live_server from webdriver 
    def test_admin_page(self, live_server):
        self.driver.get(f"{live_server.url}/admin/")
        assert "Log in | Django site admin" in self.driver.title
