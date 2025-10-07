import os
import pytest
import allure

from dotenv import load_dotenv
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FFservice
from selenium.webdriver.chrome.service import Service as CHservice
from selenium.webdriver.edge.service import Service as EDservice
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# load the url from .env
load_dotenv()
url = os.getenv('ADMIN_URL')

# parameterized fixture for browsers based on request
@pytest.fixture(params=["chrome", "firefox"], scope="class")
def get_browser(request):
    global browser
    # global browserName
    if request.param == "chrome":
        browser = webdriver.Chrome(service=CHservice(ChromeDriverManager().install()))
    if request.param == "firefox":
        browser = webdriver.Firefox(service=FFservice(GeckoDriverManager().install()))
    if request.param == "edge":
        browser = webdriver.Edge(service=EDservice(EdgeChromiumDriverManager().install()))
    request.cls.browser = browser
    browser.get(url)
    browser.maximize_window()
    # browserName = browser.current_window_handle
    yield browser
    allure.attach(browser.get_screenshot_as_png(), name="lastLook.png", attachment_type=AttachmentType.PNG)
    browser.quit()

# hook that generates failure report
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

# fixture that takes screenshot
@pytest.fixture()
def failure_screenshot(request):
    yield
    item = request.node
    if item.rep_call.failed:
        allure.attach(browser.get_screenshot_as_png(), name="failure.png", attachment_type=AttachmentType.PNG)
