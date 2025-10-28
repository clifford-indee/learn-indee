import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.pages.basePage import BasePage
from tests.params import LOGIN_TITLE
from tests.params import LONG_WAIT
from tests.params import SHORT_WAIT
from utils import configReader as CReader
from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)


class AdminLoginPage(BasePage):

    # Initialize explicit wait and inherit the browser from BasePage
    def __init__(self, browser):
        super().__init__(browser)
        self.wait = WebDriverWait(self.browser, 10)
        self.longWait = WebDriverWait(self.browser, LONG_WAIT)
        self.shortWait = WebDriverWait(self.browser, SHORT_WAIT)

    # open the SaaS login page
    def open_saas_login(self, url):
        self.browser.get(url)

    # click on sign up link
    def click_sign_up(self):
        BasePage.wait_for_foldingcube(self)
        log.logger.info("Clicking sign up link.")
        BasePage.click(self, "signUpLink_XPATH")

    # verify sign up page
    def verify_signup_page(self):
        BasePage.wait_for_foldingcube(self)
        try:
            log.logger.info("Verifying sign up page.")
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "signUpText_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Could not verify sign up page.")

    def fill_signup(self, email, pwd, cnf_pwd, first_name, last_name, company):
        log.logger.info("Checking visibility of the sign up elements.")
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "signUpEmail_XPATH")
                )
            )
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "signUpPwd_XPATH")
                )
            )
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "signUpCnfPwd_XPATH")
                )
            )
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "signUpFName_XPATH")
                )
            )
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "signUpLName_XPATH")
                )
            )
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "signUpCompany_XPATH")
                )
            )
            self.wait.until(
                EC.element_to_be_clickable(
                    CReader.read_config("locators", "signUpCheckbox_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Failed to fill sign up form.")
        else:
            log.logger.info("Filled sign up form.")
            BasePage.key_type(self, "signUpEmail_XPATH", email)
            BasePage.key_type(self, "signUpPwd_XPATH", pwd)
            BasePage.key_type(self, "signUpCnfPwd_XPATH", cnf_pwd)
            BasePage.key_type(self, "signUpFName_XPATH", first_name)
            BasePage.key_type(self, "signUpLName_XPATH", last_name)
            BasePage.key_type(self, "signUpCompany_XPATH", company)
            BasePage.click(self, "signUpCheckbox_XPATH")

    def click_signup_btn(self):
        log.logger.info("Clicking sign up button.")
        BasePage.click(self, "signUpBtn_XPATH")

    def verify_signup(self):
        BasePage.wait_for_foldingcube(self)
        try:
            log.logger.info("Checking if sign up succeeded.")
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "signUpSuccess_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Sign up not successful.")
            assert False

    # verify the login page load
    def verify_login_page(self):
        try:
            self.wait.until(EC.title_is(LOGIN_TITLE))
            log.logger.info("Current page as {}".format(self.browser.title))
        except Exception:
            assert False, "Not login page."

    # fill the login credentials
    def fill_login(self, acc_name, acc_key):
        BasePage.wait_for_foldingcube(self)
        try:
            log.logger.info("Checking visibility of login page elements.")
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "email_XPATH")
                )
            )
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "password_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Failed to fill login form")
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
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "loginFail_XPATH")
                )
            )
        except TimeoutError:
            try:
                self.shortWait.until(
                    EC.visibility_of_element_located(
                        CReader.read_config("locators", "accountDrop_XPATH")
                    )
                )
            except Exception:
                log.logger.exception("Invalid login did not fail.")
            else:
                log.logger.info("Login succeeded.")
        else:
            assert False, "Invalid login has failed as expected."

    # log out of account
    def log_out(self, email):
        log.logger.info("Logging out of current account {}.".format(email))
        BasePage.click(self, "accountDrop_XPATH")
        BasePage.click(self, "logoutOpt_XPATH")
