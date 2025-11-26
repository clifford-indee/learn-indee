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
scenarios("adminLogin.feature")


@given(parsers.parse("I navigate to the {login} page"))
def navigate_to_login(get_browser, login):
    AdminLoginPage(get_browser).open_saas_login(os.getenv(login))


@when("I check the page title")
def check_page_title():
    pass


@then("I should see the correct title")
def verify_login_page(get_browser):
    AdminLoginPage(get_browser).verify_login_page()


@when("I click on the Sign up link")
def click_on_signup(get_browser):
    AdminLoginPage(get_browser).click_sign_up()
    AdminLoginPage(get_browser).verify_signup_page()


@when(
    parsers.parse(
        "I fill the fields {email} {pwd}"
        " {first_name} {last_name} {company} on SignUp Page"
    )
)
def signup_cred(get_browser, email, pwd, first_name, last_name, company):
    if email.startswith("ACC_"):
        email = os.getenv(email)
    if pwd.startswith("KEY_"):
        pwd = os.getenv(pwd)
    AdminLoginPage(get_browser).fill_signup(
        email, pwd, pwd, first_name, last_name, company
    )


@when("I click on the SignUp button")
def click_on_signup_button(get_browser):
    AdminLoginPage(get_browser).click_signup_btn()


@then("I should see the success message")
def check_signup(get_browser):
    AdminLoginPage(get_browser).verify_signup()


@given(parsers.parse("I open the nimad {nimad} page"))
def open_nimad_page(get_browser, nimad):
    NimadEmailPage(get_browser).open_nimad_login(os.getenv(nimad))


@when(parsers.parse("I log into the {acc} and {key}"))
def nimad_login(get_browser, acc, key):
    NimadEmailPage(get_browser).fill_login(os.getenv(acc), os.getenv(key))
    NimadEmailPage(get_browser).verify_login()


@when("I navigate to the email list")
def navigate_to_email_list(get_browser):
    NimadEmailPage(get_browser).open_emails()


@then(parsers.parse("I should see the {email} has been initiated"))
def check_email_initiated(get_browser, email):
    NimadEmailPage(get_browser).verify_email(email)


@when(parsers.parse("I fill the valid {email} and {password}"))
def fill_login_cred(get_browser, email, password):
    if email.startswith("ACC_"):
        email = os.getenv(email)
    if password.startswith("KEY_"):
        password = os.getenv(password)
    AdminLoginPage(get_browser).fill_login(email, password)


@when("I click on the login button")
def click_on_login_button(get_browser):
    AdminLoginPage(get_browser).click_login_btn()


@then("I should see an error message as failure")
def check_login(get_browser):
    AdminLoginPage(get_browser).verify_login()


@when(parsers.parse("I fill the invalid {email} and {password}"))
def invalid_login_credentials(get_browser, email, password):
    AdminLoginPage(get_browser).fill_login(email, password)


@then(parsers.parse("I should see the main page and log out {email}"))
def logout_after_login(get_browser, email):
    AdminLoginPage(get_browser).log_out(email)
