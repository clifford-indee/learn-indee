from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import configReader as CReader
from tests.pages.basePage import BasePage
from tests.params import LONG_WAIT, SHORT_WAIT, LOGIN_TITLE

class AdminLoginPage(BasePage):

    def __init__(self, browser):
        super().__init__(browser)
        self.wait = WebDriverWait(self.browser, 10)
        self.longWait = WebDriverWait(self.browser, LONG_WAIT)
        self.shortWait = WebDriverWait(self.browser, SHORT_WAIT)

    # verify the login page load
    def verifyLoginPage(self):
        BasePage.waitForFoldingcube(self)
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH,
                    CReader.readConfig("locators","signInBtn_XPATH"))))
        except Exception as e:
            print("Login page not clickable.", e)
        else:
            print("Login page verified.")

    # fill the login credentials
    def fillLogin(self, acc_name, acc_key):
        BasePage.waitForFoldingcube(self)
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH,
                    CReader.readConfig("locators","email_XPATH"))))
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH,
                    CReader.readConfig("locators","password_XPATH"))))
        except Exception as e:
            raise e
        else:
            BasePage.keyType(self, "email_XPATH", acc_name)
            BasePage.keyType(self, "password_XPATH", acc_key)
            BasePage.click(self, "signInBtn_XPATH")

    # verify successful login
    def verifyLogin(self):
        BasePage.waitForFoldingcube(self)
        try:
            self.shortWait.until(
                EC.visibility_of_element_located((By.XPATH,
                    CReader.readConfig( "locators","loginFail_XPATH"))))
        except Exception as e:
            print("Successful login.")
        else:
            assert False, "Login failed."