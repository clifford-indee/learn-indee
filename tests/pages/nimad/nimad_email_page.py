import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.pages.basePage import BasePage
from tests.params import LONG_WAIT
from tests.params import NIMAD_TITLE
from tests.params import SHORT_WAIT
from utils import configReader as CReader
from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)


class NimadEmailPage(BasePage):

    # Initialize explicit wait and inherit the browser from BasePage
    def __init__(self, browser):
        super().__init__(browser)
        self.wait = WebDriverWait(self.browser, 10)
        self.longWait = WebDriverWait(self.browser, LONG_WAIT)
        self.shortWait = WebDriverWait(self.browser, SHORT_WAIT)

    # Open the Nimad login
    def open_nimad_login(self, url):
        try:
            self.browser.get(url)
        except Exception:
            log.logger.exception("Website did not load.")

    # Fill login credentials
    def fill_login(self, account, password):
        log.logger.info("Filling the nimad login.")
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "nimadAccount_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Failed to fill the nimad login.")
        else:
            log.logger.info("Login filled successfully.")
            BasePage.key_type(self, "nimadAccount_XPATH", account)
            BasePage.key_type(self, "nimadPassword_XPATH", password)
            BasePage.click(self, "nimadLoginBtn_XPATH")

    # Verify the nimad login
    def verify_login(self):
        log.logger.info("Verifying the nimad login.")
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "nimadLanding_XPATH")
                )
            )
        except Exception:
            pass
        log.logger.info("Current page as {}".format(self.browser.title))
        assert self.browser.title == NIMAD_TITLE, "Nimad login failed."

    # Navigate to the email section
    def open_emails(self):
        log.logger.info("Opening emails in nimad.")
        self.browser.get(self.browser.current_url + "post_office/email")

    """
    Verify the email sent.
    The locator is defaulted to an unindexed row
    so add the desired index as a string.
    Append as "[index]/locator"
    """

    def verify_email(self, email):
        log.logger.info("Verifying the email in nimad.")
        try:
            # flake8 is rude.
            locator = CReader.read_config(
                "locators", "nimadEmails_XPATH", "[1]/td[2]"
            )  # noqa: E501
            ele = self.wait.until(
                EC.visibility_of_element_located(locator)
            )  # noqa: E501
        except Exception:
            log.logger.exception("Failed to find the email locator.")
        else:
            assert ele.text == email, "Email doesn't match."
            # flake8 is very rude.
            locator = CReader.read_config(
                "locators", "nimadIDs_XPATH", "[1]/th/a"
            )  # noqa: E501
            self.wait.until(EC.element_to_be_clickable(locator)).click()
            try:
                locator = CReader.read_config(
                    "locators", "nimadVerify_XPATH"
                )  # noqa: E501
                self.wait.until(EC.element_to_be_clickable(locator)).click()
            except Exception:
                log.logger.exception("Failed to verify.")

    #
    def fail_email(self, email):
        log.logger.info("Locating the fail attempt email in nimad.")
        try:
            locator = CReader.read_config(
                "locators", "nimadEmails_XPATH", "[1]/td[2]"
            )  # noqa: E501
            ele = self.wait.until(
                EC.visibility_of_element_located(locator)
            )  # noqa: E501
        except Exception:
            log.logger.exception("Failed to find the email locator.")
        else:
            assert ele.text == email, "Email doesn't match."
            locator = CReader.read_config(
                "locators", "nimadIDs_XPATH", "[1]/th/a"
            )  # noqa: E501
            self.wait.until(EC.element_to_be_clickable(locator)).click()
            ele = self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "nimadSubject_XPATH")
                )
            )
            assert "Invalid login" in ele.text, "Fail subject is not valid."

    #
    def verify_video(self, email):
        log.logger.info("Verifying the video in nimad.")
        try:
            locator = CReader.read_config(
                "locators", "nimadEmails_XPATH", "[1]/td[2]"
            )  # noqa: E501
            ele = self.wait.until(
                EC.visibility_of_element_located(locator)
            )  # noqa: E501
        except Exception:
            log.logger.exception("Failed to find the email locator.")
        else:
            assert ele.text == email, "Email doesn't match."
            locator = CReader.read_config(
                "locators", "nimadIDs_XPATH", "[1]/th/a"
            )  # noqa: E501
            self.wait.until(EC.element_to_be_clickable(locator)).click()
            ele = self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "nimadSubject_XPATH")
                )
            )
            assert "Video" in ele.text, "Fail subject is not valid."
