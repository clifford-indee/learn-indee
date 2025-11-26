import os

from dotenv import load_dotenv
from pytest_bdd import scenarios, given, when, then, parsers
from tests.conftest import get_browser
from tests.pages.adminProjectsPage import AdminProjectsPage
from tests.pages.adminSendScreenerPage import AdminScreenerPage
from tests.pages.adminVideoPage import AdminVideoPage
from tests.pages.nimad.nimad_email_page import NimadEmailPage

load_dotenv()

# Load the feature file
scenarios("adminSendScreener.feature")


# T13: Admin signs into the login page with valid credentials
@given(parsers.parse("I navigate to screeners {login} page"))
def navigate_screener_login(get_browser, login):
    AdminScreenerPage(get_browser).open_saas_screener(os.getenv(login))


@when(parsers.parse("I fill account {email} and {password} for screeners"))
def fill_screener_login(get_browser, email, password):
    if email.startswith("ACC_"):
        email = os.getenv(email)
    if password.startswith("KEY_"):
        password = os.getenv(password)
    AdminScreenerPage(get_browser).fill_login(email, password)


@when("I click to submit login")
def click_screener_login_button(get_browser):
    AdminScreenerPage(get_browser).click_login_btn()


@then("I should see landing project page")
def verify_main_page(get_browser):
    AdminScreenerPage(get_browser).verify_login()


# T12: Admin receives email that the video transcoding is complete
@given(parsers.parse("I open nimad {nimad} page"))
def open_nimad_page(get_browser, nimad):
    NimadEmailPage(get_browser).open_nimad_login(os.getenv(nimad))


@when(parsers.parse("I login using nimad {account} and {password}"))
def nimad_login(get_browser, account, password):
    NimadEmailPage(get_browser).fill_login(os.getenv(account), os.getenv(password))
    NimadEmailPage(get_browser).verify_login()


@when("I navigate to the email list")
def navigate_to_email_list_for(get_browser):
    NimadEmailPage(get_browser).open_emails()


@then(parsers.parse("I should receive the video encoding completion email for {email}"))
def verify_video_encoding_email(get_browser, email):
    if email.startswith("ACC_"):
        email = os.getenv(email)
    NimadEmailPage(get_browser).verify_video(email)


# T14: Admin searches for the project and navigates to it
@given("I am at the projects page")
def at_projects_page(get_browser):
    AdminProjectsPage(get_browser).verify_project_page()


@when(parsers.parse("I use search bar for project {project}"))
def search_for_project(get_browser, project: str):
    AdminScreenerPage(get_browser).search_project(project)


@when("I click on the first result project")
def click_first_result(get_browser):
    AdminScreenerPage(get_browser).click_on_project()


@then("I should get redirected to the project's video page")
def verify_project_video_page(get_browser):
    AdminVideoPage(get_browser).verify_video_page()


# T15: Admin sends a screener room via email
@given("I am on the send screener page")
def navigate_to_send_screener_page(get_browser):
    AdminScreenerPage(get_browser).navigate_to_send_screen()


@when("I choose all videos")
def choose_all_videos(get_browser):
    # AdminScreenerPage(get_browser).select_all_videos()
    pass


@when(
    parsers.parse(
        "I fill the screener fields {views} {startdate} {starttime} {enddate} {endtime} {security} {watermarktype} for email"
    )
)
def fill_screener_email_fields(
    get_browser, views, startdate, starttime, enddate, endtime, security, watermarktype
):
    AdminScreenerPage(get_browser).fill_screeners(views, security, watermarktype)


@when("I click on screener continue button")
def click_continue_button(get_browser):
    AdminScreenerPage(get_browser).click_continue_button()


@when(parsers.parse("I fill the recipient fields {email} {watermark} {name}"))
def fill_recipient_fields(get_browser, email, watermark: str, name):
    AdminScreenerPage(get_browser).fill_recipient(email, watermark, name)


@when("I click on send email button to screener")
def click_send_email_button(get_browser):
    AdminScreenerPage(get_browser).click_send_email()


@then("I should see screener result page with the correct email")
def verify_screener_result_page(get_browser):
    AdminScreenerPage(get_browser).verify_send_screener()


# T16: Admin confirms the screener room is sent
@given("I sent a screener room")
def sent_screener_room(get_browser):
    pass


@given("I switch to the Screeners room tab")
def navigate_to_screeners_tab(get_browser):
    AdminScreenerPage(get_browser).navigate_to_screener()


@when(parsers.parse("I search the screener room list for {recipient}"))
def check_screener_room_list(get_browser, recipient: str):
    AdminScreenerPage(get_browser).find_recipient(recipient)


@then("I should see result screener room")
def enter_screener_room(get_browser):
    AdminScreenerPage(get_browser).verify_screener_room()


# T17: User receives the screener email
@given("I am already logged in nimad")
def am_logged_in(get_browser):
    # This step assumes the user is already logged in from a previous scenario
    pass


@then(parsers.parse("I should see that the user {email} received the screener email"))
def verify_user_received_screener_email(get_browser, email):
    NimadEmailPage(get_browser).verify_email(email)
