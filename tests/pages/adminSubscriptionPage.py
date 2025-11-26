import logging

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import configReader as CReader
from tests.pages.basePage import BasePage
from tests.params import LONG_WAIT, SHORT_WAIT, SUBSCRIPTION_TITLE
from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)


class AdminSubscriptionPage(BasePage):

    # Initialize explicit wait and inherit the browser from BasePage
    def __init__(self, browser):
        super().__init__(browser)
        self.wait = WebDriverWait(self.browser, 10)
        self.longWait = WebDriverWait(self.browser, LONG_WAIT)
        self.shortWait = WebDriverWait(self.browser, SHORT_WAIT)

    # verify the subscription page
    def verify_sub_page(self):
        BasePage.wait_for_foldingcube(self)
        page_title = self.browser.title
        log.logger.info("Current page as {}".format(page_title))
        assert SUBSCRIPTION_TITLE in page_title, "Not subscription page."

    # use the sidebar to move to subscription page
    def navigate_sub_page(self):
        log.logger.info("Navigate to subscription tab")
        BasePage.wait_for_foldingcube(self)
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "plansTab_XPATH")
            )
        ).click()

    # choose the premium plan/button
    def click_premium(self):
        log.logger.info("Click premium plan.")
        self.wait.until(
            EC.element_to_be_clickable(
                CReader.read_config("locators", "premiumBtn_XPATH")
            )
        ).click()

    # choose the high security plan/button
    def click_high_security(self):
        log.logger.info("Click high security plan.")
        self.wait.until(
            EC.element_to_be_clickable(
                CReader.read_config("locators", "highSecBtn_XPATH")
            )
        ).click()

    # choose the theatrical plan/button
    def click_theatrical(self):
        log.logger.info("Click theatrical plan.")
        self.wait.until(
            EC.element_to_be_clickable(
                CReader.read_config("locators", "theatricalBtn_XPATH")
            )
        ).click()

    # choose the free trail plan/buttton
    def click_trial(self):
        log.logger.info("Click trial plan.")
        self.wait.until(
            EC.element_to_be_clickable(
                CReader.read_config("locators", "trialBtn_XPATH")
            )
        ).click()

    # confirm the plan button
    def click_confirm_pre(self):
        log.logger.info("Click confirm premium plan.")
        BasePage.click(self, "premiumConfirm_XPATH")

    # confirm the plan button
    def click_confirm_high(self):
        log.logger.info("Click confirm high security plan.")
        BasePage.click(self, "premiumConfirm_XPATH")

    # confirm the plan button
    def click_confirm_the(self):
        log.logger.info("Click confirm theatrical plan.")
        BasePage.click(self, "premiumConfirm_XPATH")

    # verify the plan choosen
    def confirm_plan(self):
        try:
            log.logger.info("Confirming the chosen plan.")
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "planSwitch_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Failed to confirm the chosen plan.")
            assert False
