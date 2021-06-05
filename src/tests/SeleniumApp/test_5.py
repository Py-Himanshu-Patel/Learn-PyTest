import os
import pytest


def take_screenshot(driver, name):
    # first make the required dir
    os.makedirs(
        os.path.join("screenshot",  # path where to make directory
        os.path.dirname(name)       # name of new dir
        ),
        exist_ok=True				# no error if already exists
    )
    # now save the image to given dir with given name
    driver.save_screenshot(
        # fullname of path where to save ss
        os.path.join("screenshot", name)
    )


@pytest.mark.skip
@pytest.mark.usefixtures("driver_init_screenshot")
class TestScreenshot:
    def test_screenshot_admin(self, live_server):
        self.driver.get(f"{live_server.url}/admin/")
        take_screenshot(self.driver, "admin/" +
                        "admin_" + self.browser + ".png")
        assert "Log in | Django site admin" in self.driver.title
