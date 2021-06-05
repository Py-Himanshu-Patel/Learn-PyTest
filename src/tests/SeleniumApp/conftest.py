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


# fixture to run for each type of ss
@pytest.fixture(params=["chrome1980", "chrome411", "firefox"], scope="class")
def driver_init_screenshot(request):
    if request.param == "chrome1980":
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        web_driver = webdriver.Chrome(
            executable_path="./chromedriver",
            options=options
        )
        request.cls.browser = "Chrome1920x1080"
    if request.param == "chrome411":
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--window-size=411,823")
        web_driver = webdriver.Chrome(
            executable_path="./chromedriver",
            options=options
        )
        request.cls.browser = "Chrome411x823"
    if request.param == "firefox":
        options = webdriver.FirefoxOptions()
        options.headless = True
        web_driver = webdriver.Firefox(
            executable_path="./geckodriver",
            options=options
        )
        request.cls.browser = "Firefox"

    request.cls.driver = web_driver
    yield 
    web_driver.close()
