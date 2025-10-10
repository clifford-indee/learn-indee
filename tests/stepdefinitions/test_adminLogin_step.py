import os

from dotenv import load_dotenv
from pytest_bdd import given
from pytest_bdd import parsers
from pytest_bdd import scenarios
from pytest_bdd import then
from pytest_bdd import when

from tests.pages.adminLoginPage import AdminLoginPage
from tests.pages.nimad.nimad_email_page import NimadEmailPage

load_dotenv()
acc_name = os.getenv("ACC_THE")
acc_key = os.getenv("KEY_THE")
url = os.getenv("ENTERPRISE_URL")
nimad_acc = os.getenv("NIMAD_ACC")
nimad_key = os.getenv("NIMAD_KEY")
nimad = os.getenv("ENTERPRISE_NIMAD")

# Load the feature file
scenarios("../features/adminLogin.feature")


@given("I navigate to the login page")
def navigate_to_login(get_browser):
    AdminLoginPage(get_browser).open_saas_login(url)


@when("I check the page title")
def check_page_title(get_browser):
    AdminLoginPage(get_browser).verify_login_page()


@then(parsers.parse("I should see the correct {valid_title}"))
def verify_login_page(get_browser, valid_title):
    AdminLoginPage(get_browser).verify_login_page()


@when("I click on the Sign up link")
def click_on_signup(get_browser):
    AdminLoginPage(get_browser).click_sign_up()
    AdminLoginPage(get_browser).verify_login_page()


@when(
    parsers.parse(
        "I fill the fields {email} {pwd} {cnf_pwd}"
        " {first_name} {last_name} {company} on SignUp Page"
    )
)
def signup_credentials(
    get_browser, email, pwd, cnf_pwd, first_name, last_name, company
):
    AdminLoginPage(get_browser).fill_signup(
        email, pwd, cnf_pwd, first_name, last_name, company
    )


@when("I click on the SignUp button")
def click_on_signup_button(get_browser):
    AdminLoginPage(get_browser).click_signup_btn()


@then("I should see the success message")
def check_signup(get_browser):
    AdminLoginPage(get_browser).verify_signup()


@given("I open the nimad page")
def open_nimad_page(get_browser):
    NimadEmailPage.open_nimad_login(get_browser, nimad)


@when(parsers.parse("I log into the {account} and {password}"))
def nimad_login(get_browser, account, password):
    NimadEmailPage.fill_login(get_browser, account, password)
    NimadEmailPage.verify_login(get_browser)


@when("I navigate to the email list")
def navigate_to_email_list(get_browser):
    NimadEmailPage.open_emails(get_browser)


@then(parsers.parse("I should see the {email} initiated"))
def check_email_initiated(get_browser, email):
    NimadEmailPage.verify_email(get_browser, email)


@when(parsers.parse("I fill the valid {email} and {password}"))
def fill_login_credentials(get_browser, email, password):
    AdminLoginPage(get_browser).fill_login(email, password)


@when("I click on the login button")
def click_on_login_button(get_browser):
    AdminLoginPage(get_browser).click_login_btn()


@then("I should see an error message as failure")
@then("I should see the main page")
def check_login(get_browser):
    AdminLoginPage(get_browser).verify_login()


@when(parsers.parse("I fill the invalid {email} and {password}"))
def invalid_login_credentials(get_browser, email, password):
    AdminLoginPage(get_browser).fill_login(email, password)
