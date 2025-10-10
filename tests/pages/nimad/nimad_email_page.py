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
        self.browser.get(url)

    # Fill login credentials
    def fill_login(self, account, password):
        log.logger.info("Filling the nimad login.")
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "nimadAccount_XPATH")
                )
            )
        except Exception as e:
            log.logger.error("Failed to fill the nimad login.", e)
        else:
            log.logger.info("Login filled successfully.")
            BasePage.key_type(self, "nimadAccount_XPATH", account)
            BasePage.key_type(self, "nimadPassword_XPATH", password)
            BasePage.click(self, "nimadLoginBtn_XPATH")

    # Verify the nimad login
    def verify_login(self):
        log.logger.info("Verifying the nimad login.")
        assert self.browser.title == NIMAD_TITLE, "Nimad login failed."

    # Navigate to the email section
    def open_emails(self):
        log.logger.info("Opening emails in nimad.")
        self.browser.get(self.browser.current_url + "post_office/email")

    """
    Verify the email sent.
    The locator is defaulted to an unindexed row,
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
            assert ele.text == email, "Email doesn't match."
        except Exception as e:
            log.logger.error("Failed to find the email locator.", e)
        else:
            # flake8 is very rude.
            locator = CReader.read_config(
                "locators", "nimadIDs_XPATH", "[1]/th/a"
            )  # noqa: E501
            self.wait.until(EC.element_to_be_clickable(locator)).click()
            self.wait.until(
                EC.element_to_be_clickable(
                    CReader.read_config("locators", "nimadVerify_XPATH")
                )
            ).click()  # noqa: E501
            try:
                locator = CReader.read_config(
                    "locators", "nimadVerifyBtn_XPATH"
                )  # noqa: E501
                self.wait.until(EC.element_to_be_clickable(locator))
            except Exception as e:
                log.logger.error("Failed to verify.", e)
