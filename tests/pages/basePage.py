import logging

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import configReader as CReader
from tests.params import LONG_WAIT, SHORT_WAIT
from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)

# base page functions that are commonly used
class BasePage:

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser,10)
        self.longWait = WebDriverWait(self.browser, LONG_WAIT)
        self.shortWait = WebDriverWait(self.browser, SHORT_WAIT)

    # clicking on an element
    def click(self, locator):
        log.logger.info("Clicking on element:{}".format(locator))
        try:
            self.wait.until(
                EC.element_to_be_clickable(
                    CReader.read_config("locators", locator))).click()
        except Exception as e:
            print("Click failed.", e)

    # entering keyboard values
    def key_type(self, locator, text: str):
        log.logger.info("Key type on element:{} text:{}".format(locator, text))
        try:
            self.wait.until(
                EC.element_to_be_clickable(
                    CReader.read_config("locators", locator))).send_keys(text)
        except Exception as e:
            print("Type failed.", e)

    # wait for page loading
    def wait_for_foldingcube(self):
        log.logger.info("Waiting for the folding cube.")
        try:
            self.longWait.until(
                EC.invisibility_of_element_located(
                    CReader.read_config("locators", "foldingCube_XPATH")))
        except Exception as e:
            print("Loading failed", e)