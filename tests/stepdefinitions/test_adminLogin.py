"""
Author: Clifford @indee
Test cases for SaaS login page.
"""

import logging
import os

import pytest
from dotenv import load_dotenv
from tests.pages.adminLoginPage import AdminLoginPage
from tests.stepdefinitions.baseTest import BaseTest
from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)


# class level test
@pytest.mark.skip(reason="Non BDD tests.")
class TestAdminLogin(BaseTest):

    # load the credentials from the .env
    load_dotenv()
    acc_name = os.getenv("ACC_THE")
    acc_key = os.getenv("KEY_THE")

    # test to validate the page title
    def test_validate_login(self):
        log.logger.info("Test to validate login page title.")
        loginPg = AdminLoginPage(self.browser)
        loginPg.verify_login_page()
        log.logger.info("Test successful.")

    # functional test to enter login credentials, by calling page
    def test_login(self):
        log.logger.info("Test to fill valid login credentials.")
        loginPg = AdminLoginPage(self.browser)
        loginPg.fill_login(self.acc_name, self.acc_key)
        log.logger.info("Test successful.")

    # negative test to enter wrong credentials
    @pytest.mark.negative
    def test_invalid_login(self):
        log.logger.info("Test to fill invalid login credentials.")
        invalid_acc = "invalid@indee.tv"
        invalid_key = "12345"
        loginPg = AdminLoginPage(self.browser)
        loginPg.fill_login(invalid_acc, invalid_key)
        loginPg.verify_login()
        log.logger.info("Test successful.")
