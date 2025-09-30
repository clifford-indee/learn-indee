import os

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import configReader as CR
from tests.pages.basePage import basePage

class adminloginPage(basePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(self.driver,10)

    def verifyLogin(self):
        basePage.waitForFoldingcube(self)
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    CR.readConfig("locators","signInBtn_XPATH")))
        except Exception as e:
            print("Login page bug.", e)
        else:
            print("Login page verified.")

    def fillLogin(self):
        load_dotenv()
        acc_name = os.getenv('ACC_THE')
        acc_key = os.getenv('KEY_THE')
        basePage.waitForFoldingcube(self)
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    CR.readConfig("locators","email_XPATH")))
            self.wait.until(
                EC.visibility_of_element_located(
                    CR.readConfig("locators","password_XPATH")))
        except Exception as e:
            print(e)
        else:
            self.keyType("email_XPATH", acc_name)
            self.keyType("password_XPATH", acc_key)
            self.click("signInBtn_XPATH")