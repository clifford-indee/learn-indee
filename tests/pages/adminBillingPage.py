import logging

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import configReader as CReader
from tests.pages.basePage import BasePage
from tests.params import LONG_WAIT, SHORT_WAIT, BILLING_TITLE
from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)


class AdminBillingPage(BasePage):

    # initialize explicit wait and inherit the browser from BasePage
    def __init__(self, browser):
        super().__init__(browser)
        self.wait = WebDriverWait(self.browser, 10)
        self.longWait = WebDriverWait(self.browser, LONG_WAIT)
        self.shortWait = WebDriverWait(self.browser, SHORT_WAIT)

    # verify the title of the page loaded (not UI)
    def verify_billing_page(self):
        log.logger.info("Current page as {}".format(self.browser.title))
        assert BILLING_TITLE in self.browser.title, "Not billing page."

    # redirect to the billing by interacting
    def redirect_to_billing(self):
        curr_window = self.browser.current_window_handle
        BasePage.click(self, "accountDrop_XPATH")
        BasePage.click(self, "billingOpt_XPATH")
        self.wait.until(EC.number_of_windows_to_be(2))
        for window_handle in self.browser.window_handles:
            if window_handle != curr_window:
                self.browser.switch_to.window(window_handle)
                break

    # fill the billing details on the page
    def fill_bill(
        self,
        firstname,
        lastname,
        cardnumber,
        expiryyear,
        expirymonth,
        cvv,
        country,
        street,
        city,
        postal,
    ):
        log.logger.info("Checking visibility of the sign up elements.")
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "billFName_XPATH")
            )
        ).clear()
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "billLName_XPATH")
            )
        ).clear()
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "billCardNum_XPATH")
            )
        ).send_keys(cardnumber)
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "billCVV_XPATH")
            )
        ).send_keys(cvv)
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "billStreet_XPATH")
            )
        ).clear()
        # why do we use flake8
        loc = CReader.read_config("locators", "billCountySelect_XPATH")
        ctyDrp = Select(self.wait.until(EC.visibility_of_element_located(loc)))
        ctyDrp.select_by_visible_text(country)
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "billCity_XPATH")
            )
        ).clear()
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "billPostal_XPATH")
            )
        ).clear()
        BasePage.key_type(self, "billFName_XPATH", firstname)
        BasePage.key_type(self, "billLName_XPATH", lastname)
        BasePage.key_type(self, "billStreet_XPATH", street)
        BasePage.key_type(self, "billCity_XPATH", city)
        BasePage.key_type(self, "billPostal_XPATH", postal)
        log.logger.info("Filled billing form.")

    # click the confirm bill button after successful filling
    def click_confirm_bill(self):
        log.logger.info("Clicking the confirm button.")
        BasePage.click(self, "billConfirmBtn_XPATH")

    # verify the success of the billing details and change windows
    def bill_success(self):
        other_window = None
        status = True
        try:
            log.logger.info("Checking if billing is completed.")
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "billSuccess_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Failed to update billing form.")
            status = False
        try:
            curr_window = self.browser.current_window_handle
            for window_handle in self.browser.window_handles:
                if window_handle != curr_window:
                    other_window = window_handle
                    break
            self.browser.close()
            self.browser.switch_to.window(other_window)
        except Exception:
            log.logger.exception("Failed to redirect to billing page.")
        else:
            assert status, "Billing page failed."
