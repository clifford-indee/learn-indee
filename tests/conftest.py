import logging
import os

import allure
import pytest
from allure_commons.types import AttachmentType
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as CHservice
from selenium.webdriver.edge.service import Service as EDservice
from selenium.webdriver.firefox.service import Service as FFservice
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)

# load the url from .env
load_dotenv()
url = os.getenv("ENTERPRISE_URL")


# parameterized fixture for browsers based on request
@pytest.fixture(params=["chrome", "firefox"], scope="class")
# @pytest.fixture(params=["chrome", "firefox"], scope="function", autouse=True)
def get_browser(request):
    global browser
    if request.param == "chrome":
        service = CHservice(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service)
    if request.param == "firefox":
        service = FFservice(GeckoDriverManager().install())
        browser = webdriver.Firefox(service=service)
    if request.param == "edge":
        browser = webdriver.Edge(
            service=EDservice(EdgeChromiumDriverManager().install())
        )
    request.cls.browser = browser
    # browser.get(url)
    browser.maximize_window()
    log.logger.info("Loading browser {}".format(browser.current_window_handle))
    yield browser
    allure.attach(
        browser.get_screenshot_as_png(),
        name="lastLook.png",
        attachment_type=AttachmentType.PNG,
    )
    browser.quit()


# hook that generates failure report
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


# fixture that takes screenshot when test call has failed
@pytest.fixture()
def failure_screenshot(request):
    yield
    item = request.node
    if item.rep_call.failed:
        allure.attach(
            browser.get_screenshot_as_png(),
            name="failure.png",
            attachment_type=AttachmentType.PNG,
        )
