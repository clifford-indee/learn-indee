import logging
from pathlib import Path

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import configReader as CReader
from tests.pages.basePage import BasePage
from tests.params import LONG_WAIT, SHORT_WAIT, VIDEO_TITLE
from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)


class AdminVideoPage(BasePage):

    # initialize explicit wait and inherit the browser from BasePage
    def __init__(self, browser):
        super().__init__(browser)
        self.wait = WebDriverWait(self.browser, 10)
        self.longWait = WebDriverWait(self.browser, LONG_WAIT)
        self.shortWait = WebDriverWait(self.browser, SHORT_WAIT)

    # verify the video page loaded
    def verify_video_page(self):
        BasePage.wait_for_foldingcube(self)
        BasePage.wait_for_loadbar(self)
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "addVideoText_XPATH")
                )
            )
        except Exception:
            pass
        log.logger.info("Current page as {}".format(self.browser.title))
        assert VIDEO_TITLE in self.browser.title, "Not videos page."
        self.wait.until(
            EC.element_to_be_clickable(
                CReader.read_config("locators", "planEleOverhead_XPATH")
            )
        ).click()

    # use the sidebar to move to videos page
    def navigate_video_page(self):
        BasePage.wait_for_foldingcube(self)
        log.logger.info("Navigate to video tab.")
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "videoTab_XPATH")
            )
        ).click()

    # if no video exists, add a new video
    def click_on_new_video(self):
        try:
            log.logger.info("Click on new video.")
            self.shortWait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "addNewVideo_XPATH")
                )
            ).click()
        except TimeoutException:
            try:
                self.shortWait.until(
                    EC.visibility_of_element_located(
                        CReader.read_config("locators", "addVideo_XPATH")
                    )
                ).click()
            except Exception:
                log.logger.exception("Failed to click on new video.")

    # fill the video details
    def fill_video_form(
        self, name, video, roughcut: bool, internalnotes, hi_res, subtitle
    ):
        log.logger.info("Filling video form.")
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "videoName_XPATH")
            )
        ).send_keys(name)
        video_ele = self.wait.until(
            EC.presence_of_element_located(
                CReader.read_config("locators", "videoUpload_XPATH")
            )
        )
        ele = self.wait.until(
            EC.presence_of_element_located(
                CReader.read_config("locators", "videoRoughCut_XPATH")
            )
        )
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "videoIntNotes_XPATH")
            )
        ).send_keys(internalnotes)
        self.wait.until(
            EC.presence_of_element_located(
                CReader.read_config("locators", "videoHiRes_XPATH")
            )
        )
        self.wait.until(
            EC.presence_of_element_located(
                CReader.read_config("locators", "videoSub_XPATH")
            )
        )
        base = Path(__file__).parent.parent.parent / "sample" / video
        video_ele.send_keys(str(base))
        if roughcut:
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", ele
            )
            self.browser.execute_script("arguments[0].click();", ele)
        log.logger.info("Successfully filled video form.")

    # click the upload video button
    def click_upload(self):
        log.logger.info("Click on video upload button.")
        BasePage.click(self, "videoUploadBtn_XPATH")

    # verify if the upload is successful
    def verify_upload(self):
        BasePage.wait_for_foldingcube(self)
        log.logger.info("Verifying video upload success.")
        try:
            self.longWait.until(
                EC.visibility_of_element_located(
                    CReader.read_config("locators", "uploadSuccess_XPATH")
                )
            )
        except Exception:
            log.logger.exception("Failed to upload video.")
            assert False, "Failed to upload video."

    # fill the watermark details after video details
    def fill_watermark(self, opacity):
        BasePage.wait_for_foldingcube(self)
        log.logger.info("Filling watermark.")
        self.wait.until(
            EC.presence_of_element_located(
                CReader.read_config("locators", "watermarkGrid_XPATH")
            )
        )
        self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "watermarkSlide_XPATH")
            )
        )
        loc = CReader.read_config("locators", "WatermarkFreqAlways_XPATH")
        self.wait.until(EC.visibility_of_element_located(loc))
        BasePage.slider(self, "watermarkGrid_XPATH", int(opacity) - 60)
        log.logger.info("Successfully filled watermark.")

    # click the save video buttton
    def click_save(self):
        log.logger.info("Click on video save button.")
        BasePage.click(self, "videoSaveBtn_XPATH")

    # verify completion of video upload
    def upload_complete(self, video: str):
        BasePage.wait_for_foldingcube(self)
        log.logger.info("Verifying upload.")
        ele = self.wait.until(
            EC.visibility_of_element_located(
                CReader.read_config("locators", "firstVideo_XPATH")
            )
        )
        assert ele.text == video, "Failed to upload video."
