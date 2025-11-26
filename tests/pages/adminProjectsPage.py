import logging

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import configReader as CReader
from tests.pages.basePage import BasePage
from tests.params import (
    LONG_WAIT,
    SHORT_WAIT,
    LOGIN_TITLE,
    PROJECT_TITLE,
    SUBSCRIPTION_TITLE,
)
from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)


class AdminProjectsPage(BasePage):

    # initialize explicit wait and inherit the browser from BasePage
    def __init__(self, browser):
        super().__init__(browser)
        self.wait = WebDriverWait(self.browser, 10)
        self.longWait = WebDriverWait(self.browser, LONG_WAIT)
        self.shortWait = WebDriverWait(self.browser, SHORT_WAIT)

    #
    def open_saas_project(self, url):
        self.browser.get(url)
        log.logger.info("Current page as {}".format(self.browser.title))
        assert self.browser.title == LOGIN_TITLE, "Not login page."

    #
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
            log.logger.exception("Failed to fill login form.")
        else:
            log.logger.info("Login page filled.")
            BasePage.key_type(self, "email_XPATH", acc_name)
            BasePage.key_type(self, "password_XPATH", acc_key)

    # click the login button
    def click_login(self):
        log.logger.info(".Clicking login button")
        BasePage.click(self, "signInBtn_XPATH")

    # verify the login page load
    def verify_project_page(self):
        BasePage.wait_for_foldingcube(self)
        log.logger.info("Current page as {}".format(self.browser.title))
        assert self.browser.title == PROJECT_TITLE, "Not project page."

    # create a new project, not the first time link
    def create_new_project(self):
        log.logger.info("Creating new project.")
        BasePage.wait_for_foldingcube(self)
        try:
            self.shortWait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "firstProject_XPATH")
                )
            ).click()
        except Exception:
            try:
                loc = "createNewProjectBtn_XPATH"
                self.wait.until(
                    EC.visibility_of_element_located(
                        CReader.read_config("locators", loc)
                    )
                ).click()
            except Exception:
                log.logger.exception("Failed to create new project.")

    # fill the project details
    def fill_project(self, name: str, desc, genre):
        BasePage.wait_for_foldingcube(self)
        try:
            log.logger.info("Checking visibility of project page elements.")
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "projectName_XPATH")
                )
            )
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "projectDesc_XPATH")
                )
            )
            self.wait.until(
                EC.element_to_be_clickable(
                    CReader.read_config("locators", "projectGenre_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Failed to fill project details.")
        else:
            log.logger.info("Project page filled.")
            fullname = name.format(self.index)
            BasePage.key_type(self, "projectName_XPATH", fullname)
            BasePage.key_type(self, "projectDesc_XPATH", desc)
            BasePage.key_type(self, "projectGenre_XPATH", genre)
            BasePage.click(self, "projectGenreOpt_XPATH")

    #
    def submit_project(self):
        log.logger.info("Submitting project.")
        BasePage.click(self, "projectSubmitBtn_XPATH")

    #
    def video_skip(self):
        log.logger.info("Video skipped.")
        BasePage.click(self, "videoSkip_XPATH")

    #
    def verify_sub_page(self):
        BasePage.wait_for_loadbar(self)
        BasePage.wait_for_foldingcube(self)
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "premiumBtn_XPATH")
                )
            )
        except Exception:
            pass
        page_title = self.browser.title
        log.logger.info("Current page as {}".format(page_title))
        assert SUBSCRIPTION_TITLE in page_title, "Not subscription page."
