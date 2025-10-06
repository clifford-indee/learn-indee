'''
Author: Clifford @indee
Test cases for SaaS login page.
'''

import os
import pytest

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from tests.conftest import get_browser
from tests.pages.adminLoginPage import AdminLoginPage
from tests.stepdefinitions.baseTest import BaseTest

# class level
class Test_AdminLogin(BaseTest):

    # load the credentials from the .env
    load_dotenv()
    acc_name = os.getenv('ACC_THE')
    acc_key = os.getenv('KEY_THE')

    # test to validate the page title
    def test_validateLogin(self):
        loginPg = AdminLoginPage(self.browser)
        loginPg.verifyLoginPage()

    # functional test to enter login credentials, by calling page
    def test_login(self):
        loginPg = AdminLoginPage(self.browser)
        loginPg.fillLogin(self.acc_name, self.acc_key)

    # negative test to enter wrong credentials
    @pytest.mark.negative
    def test_invalidLogin(self):
        invalid_acc = "invalid@indee.tv"
        invalid_key = "12345"
        loginPg = AdminLoginPage(self.browser)
        loginPg.fillLogin(invalid_acc, invalid_key)
        loginPg.verifyLogin()