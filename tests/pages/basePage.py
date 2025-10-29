import logging
import random

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.params import LONG_WAIT
from tests.params import SHORT_WAIT
from utils import configReader as CReader
from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)


# base page functions that are commonly used
class BasePage:

    index = str(random.randint(1, 100))

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 10)
        self.longWait = WebDriverWait(self.browser, LONG_WAIT)
        self.shortWait = WebDriverWait(self.browser, SHORT_WAIT)

    # clicking on an element
    def click(self, locator):
        log.logger.info("Clicking on element:{}".format(locator))
        try:
            # not so friendly flake8
            locate = CReader.read_config("locators", locator)
            self.wait.until(EC.element_to_be_clickable(locate)).click()
        except Exception:
            log.logger.exception("Click failed.")

    # entering keyboard values
    def key_type(self, locator, text):
        log.logger.info("Key type on element:{} text:{}".format(locator, text))
        try:
            # not so friendly flake8
            locate = CReader.read_config("locators", locator)
            self.wait.until(EC.element_to_be_clickable(locate)).send_keys(text)
        except Exception:
            log.logger.exception("Type failed.")

    # wait for page loading
    def wait_for_foldingcube(self):
        log.logger.info("Waiting for the folding cube.")
        try:
            self.longWait.until(
                EC.invisibility_of_element_located(
                    CReader.read_config("locators", "foldingCube_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Loading failed")

    #
    def js_click(self, locator):
        log.logger.info("Javascript click on element:{}".format(locator))
        try:
            # not so friendly flake8
            locate = CReader.read_config("locators", locator)
            ele = self.wait.until(EC.presence_of_element_located(locate))
        except Exception:
            log.logger.exception("Element not found.")
        else:
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", ele
            )
            self.browser.execute_script("arguments[0].click();", ele)

    #
    def slider(self, locator, offset):
        log.logger.info("Slider move element:{}".format(locator))
        action = ActionChains(self.browser)
        try:
            locate = CReader.read_config("locators", locator)
            ele = self.wait.until(EC.visibility_of_element_located(locate))
            action.drag_and_drop_by_offset(ele, offset, 0).perform()
        except Exception:
            log.logger.exception("Slider failed.")
