import logging

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import configReader as CReader
from tests.pages.basePage import BasePage
from tests.params import LONG_WAIT, SHORT_WAIT, LOGIN_TITLE
from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)

class AdminLoginPage(BasePage):

    def __init__(self, browser):
        super().__init__(browser)
        self.wait = WebDriverWait(self.browser, 10)
        self.longWait = WebDriverWait(self.browser, LONG_WAIT)
        self.shortWait = WebDriverWait(self.browser, SHORT_WAIT)

    # verify the login page load
    def verify_login_page(self):
        # log.logger.info("Current page as {}".format(self.browser.title))
        assert self.browser.title == LOGIN_TITLE, "Not login page."

    # fill the login credentials
    def fill_login(self, acc_name, acc_key):
        BasePage.wait_for_foldingcube(self)
        try:
            log.logger.info("Checking visibility of login page elements.")
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators","email_XPATH")))
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators","password_XPATH")))
        except Exception as e:
            raise e
        else:
            log.logger.info("Login page filled.")
            BasePage.key_type(self, "email_XPATH", acc_name)
            BasePage.key_type(self, "password_XPATH", acc_key)

    # click the login button
    def click_login_btn(self):
        log.logger.info("Clicking login button.")
        BasePage.click(self, "signInBtn_XPATH")

    # verify successful login
    def verify_login(self):
        BasePage.wait_for_foldingcube(self)
        try:
            self.shortWait.until(
                EC.visibility_of_element_located(
                    CReader.read_config( "locators","loginFail_XPATH")))
        except Exception as e:
            print("Successful login.", e)
        else:
            assert False, "Login failed."