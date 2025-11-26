import logging

from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.pages.basePage import BasePage
from tests.params import LONG_WAIT
from tests.params import SHORT_WAIT
from utils import configReader as CReader
from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)


class AdminScreenerPage(BasePage):

    # Initialize explicit wait and inherit the browser from BasePage
    def __init__(self, browser):
        super().__init__(browser)
        self.wait = WebDriverWait(self.browser, 10)
        self.longWait = WebDriverWait(self.browser, LONG_WAIT)
        self.shortWait = WebDriverWait(self.browser, SHORT_WAIT)

    # open the SaaS login page
    def open_saas_screener(self, url):
        self.browser.get(url)

    # fill the login credentials
    def fill_login(self, acc_name, acc_key):
        BasePage.wait_for_foldingcube(self)
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
        except Exception:
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
            assert False, "Invalid login has failed."

    # use the search bar to find the project
    def search_project(self, project: str):
        BasePage.wait_for_foldingcube(self)
        log.logger.info("Searching for project.")
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "projectSearch_XPATH")
            )
        ).send_keys(project.format(self.index) + Keys.ENTER)

    # click the result project after search
    def click_on_project(self):
        log.logger.info("Clicking on the project.")
        self.wait.until(
            EC.element_to_be_clickable(
                CReader.read_config("locators", "projectLink_XPATH")
            )
        ).click()

    # Wait for the video to complete transcoding
    def transcoding(self):
        BasePage.wait_for_foldingcube(self)
        try:
            self.longWait.until(
                EC.invisibility_of_element(
                    CReader.read_config("locators", "transcoding_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Transcoding failed.")

    # Use the side bar to move to send screeners
    def navigate_to_send_screen(self):
        BasePage.wait_for_foldingcube(self)
        log.logger.info("Navigating to screener.")
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "sendScreenTab_XPATH")
            )
        ).click()

    # Click on the select all videos checkbox (js retry)
    def select_all_videos(self):
        BasePage.wait_for_foldingcube(self)
        try:
            log.logger.info("Selecting all videos.")
            ele = self.wait.until(
                EC.presence_of_element_located(
                    CReader.read_config("locators", "screenerAllVideo_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Fail to select all videos.")
        else:
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", ele
            )
            self.browser.execute_script("arguments[0].click();", ele)

    # fill the screeners details
    def fill_screeners(self, views, security="None", watermarktype="None"):
        log.logger.info("Filling screeners fields.")
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "screenerTypeDrop_XPATH")
            )
        ).click()
        self.wait.until(
            EC.presence_of_element_located(
                CReader.read_config("locators", "screenerTypeEmail_XPATH")
            )
        ).click()
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "screenerViews_XPATH")
            )
        ).clear()
        self.wait.until(
            EC.presence_of_element_located(
                CReader.read_config("locators", "securityNone_XPATH")
            )
        )
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "watermarkTypeDrop_XPATH")
            )
        ).click()
        # watermark type
        if watermarktype == "Overlay":
            BasePage.click(self, "watermarkOverlay_XPATH")
        elif watermarktype == "Forensic":
            BasePage.click(self, "watermarkForensic_XPATH")
        elif watermarktype == "Burned":
            BasePage.click(self, "watermarkBurned_XPATH")
        else:
            BasePage.click(self, "watermarkNone_XPATH")
        # security type
        if security == "Password":
            BasePage.click(self, "securityPass_XPATH")
        elif security == "2FA":
            BasePage.click(self, "security2FA_XPATH")
        else:
            BasePage.js_click(self, "securityNone_XPATH")
        # BasePage.key_type(self, "screenerViews_XPATH", views)
        log.logger.info("Successfully filled screeners fields.")

    # after details, click continue button
    def click_continue_button(self):
        log.logger.info("Clicking continue button.")
        self.wait.until(
            EC.element_to_be_clickable(
                CReader.read_config("locators", "sendContinueBtn_XPATH")
            )
        ).click()

    # fill the recipient details
    def fill_recipient(self, email, watermark: str, name):
        BasePage.wait_for_foldingcube(self)
        log.logger.info("Filling recipient fields.")
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "screenerEmailInput_XPATH")
            )
        ).send_keys(email)
        loc = CReader.read_config("locators", "screenerWatermarkIn_XPATH")
        self.wait.until(EC.visibility_of_element_located(loc)).send_keys(
            watermark.format(self.index)
        )
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "screenerNameInput_XPATH")
            )
        ).send_keys(name)

    # after filling details, click the send emails button
    def click_send_email(self):
        log.logger.info("Clicking send email button.")
        self.wait.until(
            EC.element_to_be_clickable(
                CReader.read_config("locators", "sendScreenerBtn_XPATH")
            )
        ).click()

    # verify that screeners successfully sent
    def verify_send_screener(self):
        BasePage.wait_for_foldingcube(self)
        log.logger.info("Verifying whether screeners are sent.")
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "screenerSuccess_XPATH")
            )
        )

    # use the side bar to move to screeners page
    def navigate_to_screener(self):
        BasePage.wait_for_foldingcube(self)
        log.logger.info("Navigating to screener.")
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "screenersTab_XPATH")
            )
        ).click()

    """
    Locator is the recipient table.
    Add the tr[] for row and td[1] for recipient
    """

    def find_recipient(self, recipient: str):
        BasePage.wait_for_foldingcube(self)
        try:
            log.logger.info("Finding recipient.")
            ele = self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "screenerRecipient_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Failed to find recipient locator.")
        else:
            if ele.text == recipient.format(self.index):
                ele.click()
            else:
                assert False, "Failed to find recipient."

    # verify the sent screeners room
    def verify_screener_room(self):
        BasePage.wait_for_foldingcube(self)
        try:
            log.logger.info("Verifying active screeners room.")
            self.wait.until(
                EC.element_to_be_clickable(
                    CReader.read_config("locators", "updateRoomBtn_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Failed to verify active screeners room.")
            assert False, "Failed to verify active screeners room."
