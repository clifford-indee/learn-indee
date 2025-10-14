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

# Load the feature file
scenarios("../features/adminLogin.feature")


@given(parsers.parse("I navigate to the {login} page"))
def navigate_to_login(get_browser, login):
    AdminLoginPage(get_browser).open_saas_login(os.getenv(login))


@when("I check the page title")
def check_page_title(get_browser):
    pass


@then("I should see the correct title")
def verify_login_page(get_browser):
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


@given(parsers.parse("I open the {nimad} page"))
def open_nimad_page(get_browser, nimad):
    NimadEmailPage.open_nimad_login(get_browser, os.getenv(nimad))


@when(parsers.parse("I log into the {acc} and {key}"))
def nimad_login(get_browser, acc, key):
    NimadEmailPage.fill_login(get_browser, os.getenv(acc), os.getenv(key))
    NimadEmailPage.verify_login(get_browser)


@when("I navigate to the email list")
def navigate_to_email_list(get_browser):
    NimadEmailPage.open_emails(get_browser)


@then(parsers.parse("I should see the {email} has been initiated"))
def check_email_initiated(get_browser, email):
    NimadEmailPage.verify_email(get_browser, email)


@when(parsers.parse("I fill the valid {email} and {key}"))
def fill_login_credentials(get_browser, email, key):
    AdminLoginPage(get_browser).fill_login(os.getenv(email), os.getenv(key))


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
