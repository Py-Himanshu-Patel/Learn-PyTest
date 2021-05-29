import pytest
from selenium import webdriver


@pytest.fixture(scope="class")
def chrome_driver_init(request):

    options = webdriver.ChromeOptions()
    options.headless = True
    chrome_driver = webdriver.Chrome(
        executable_path="./chromedriver",
        options=options
    )
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()


# a more generic fixture can be used for both chrome as well firefox
@pytest.fixture(params=["chrome", "firefox"], scope="class")
def driver_init(request):
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options.headless = True
        web_driver = webdriver.Chrome(
            executable_path="./chromedriver",
            options=options
        )
    if request.param == "firefox":
        options = webdriver.FirefoxOptions()
        options.headless = True
        web_driver = webdriver.Firefox(
            executable_path="./geckodriver",
            options=options
        )
    request.cls.driver = web_driver
    yield 
    web_driver.close()
