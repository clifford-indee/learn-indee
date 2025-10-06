from logging import exception

from selenium import webdriver
from tests import conftest
from selenium.common import ElementClickInterceptedException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import configReader as CReader
from tests.params import LONG_WAIT, SHORT_WAIT
from selenium.webdriver.remote.webdriver import WebDriver

# base page functions that are commonly used
class BasePage:

    def __init__(self, browser):
        # self.browser: webDriver
        self.browser = browser
        self.wait = WebDriverWait(self.browser,10)
        self.longWait = WebDriverWait(self.browser, LONG_WAIT)
        self.shortWait = WebDriverWait(self.browser, SHORT_WAIT)

    # clicking on an element
    def click(self, locator):
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH,
                    CReader.readConfig("locators", locator))))
        except ElementClickInterceptedException:
            print("Click failed.")
        else:
            self.browser.find_element(By.XPATH, CReader.readConfig("locators", locator)).click()

    # entering keyboard values
    def keyType(self, locator, text: str):
        try:
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                    CReader.readConfig("locators", locator))))
        except ElementNotSelectableException:
            print("Type failed.")
        else:
            self.browser.find_element(By.XPATH, CReader.readConfig("locators", locator)).click()

    # wait for page loading
    def waitForFoldingcube(self):
        try:
            self.longWait.until(
                EC.invisibility_of_element_located((By.XPATH,
                    CReader.readConfig("locators", "foldingCube_XPATH"))))
        except Exception as e:
            print(e)