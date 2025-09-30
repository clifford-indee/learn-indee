from logging import exception

from selenium.common import ElementClickInterceptedException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import configReader as CR
from tests.params import LONG_WAIT

class basePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver,10)
        self.longWait = WebDriverWait(self.driver, LONG_WAIT)

    def click(self, locator):
        try:
            self.wait.until(
                EC.element_to_be_clickable(
                    CR.readConfig("locators", locator))).click()
        except ElementClickInterceptedException:
            print("Click failed.")

    def keyType(self, locator, text: str):
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    CR.readConfig("locators", locator))).send_keys(text)
        except ElementNotSelectableException:
            print("Type failed.")

    def waitForFoldingcube(self):
        try:
            self.longWait.until(
                EC.invisibility_of_element_located(
                    CR.readConfig("locators", "foldingCube_XPATH")))
        except Exception as e:
            print("Loading bug.", e)