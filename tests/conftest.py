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


"""
# pytest parameterized fixture for browsers based on request
@pytest.fixture(params=["chrome", "firefox"], scope="class", autouse=True)
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
"""


# custom command options for browser selection
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Select which browser to use (chrome or firefox)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode (default False)",
    )


# ensure command parameters are passed during config
def pytest_configure(config):
    if not config.getoption("--browser"):
        config.option.browser = "chrome"
    if not config.getoption("--alluredir"):
        config.option.alluredir = "allureReport"
    if not config.getoption("--headless"):
        config.option.headless = False


# new initialization hook
@pytest.fixture(scope="session")
def get_browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    browser_name = browser_name.lower()
    global browser
    browser = None
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--enable-automation")
        service = CHservice(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        service = FFservice(GeckoDriverManager().install())
        browser = webdriver.Firefox(service=service, options=options)
        browser.maximize_window()
    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless")
        service = EDservice(EdgeChromiumDriverManager().install())
        browser = webdriver.Edge(service=service, options=options)
        browser.maximize_window()
    else:
        raise ValueError("Unsupported browser: {}".format(browser_name))
    yield browser
    log.logger.info("Quit browser {}".format(browser.current_window_handle))
    browser.quit()


# browser fixture specific for chrome
@pytest.fixture(scope="session")
def chrome():
    global browser
    service = CHservice(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.maximize_window()
    log.logger.info("Loading browser {}".format(browser.current_window_handle))
    yield browser
    allure.attach(
        browser.get_screenshot_as_png(),
        name="lastLook.png",
        attachment_type=AttachmentType.PNG,
    )
    log.logger.info("Quit browser {}".format(browser.current_window_handle))
    browser.quit()


# hook that generates failure report
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            allure.attach(
                browser.get_screenshot_as_png(),
                name="Failed.png",
                attachment_type=AttachmentType.PNG,
            )
        except Exception:
            log.logger.exception("Screenshot error.")
    setattr(item, "rep_" + rep.when, rep)
    return rep


# hook to capture screenshot after each scenario
@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_scenario(request, feature, scenario):
    try:
        # Get the scenario name for better naming
        scenario_name = scenario.name.replace(" ", "_").replace(":", "")
        allure.attach(
            browser.get_screenshot_as_png(),
            name=f"scenario_end_{scenario_name}.png",
            attachment_type=AttachmentType.PNG,
        )
    except Exception:
        log.logger.exception("Screenshot error.")
