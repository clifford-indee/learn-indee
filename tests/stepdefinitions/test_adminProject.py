import os

from dotenv import load_dotenv
from pytest_bdd import scenarios, given, when, then, parsers
from tests.conftest import get_browser

from tests.pages.adminBillingPage import AdminBillingPage
from tests.pages.adminProjectsPage import AdminProjectsPage
from tests.pages.adminSubscriptionPage import AdminSubscriptionPage
from tests.pages.adminVideoPage import AdminVideoPage

load_dotenv()

# Load the feature file
scenarios("adminProjects.feature")


# T06: Admin logins to their account with project account
@given(parsers.parse("I navigate to project {login}"))
def navigate_project_login(get_browser, login):
    AdminProjectsPage(get_browser).open_saas_project(os.getenv(login))


@when(parsers.parse("I enter project account {email} and {password}"))
def fill_project_login(get_browser, alerts, email, password):
    if email.startswith("ACC_"):
        email = os.getenv(email)
    if password.startswith("KEY_"):
        password = os.getenv(password)
    AdminProjectsPage(get_browser).fill_login(email, password)


@when("I submit the login form")
def click_the_login_button(get_browser):
    AdminProjectsPage(get_browser).click_login()


@then("I should see the main page")
def verify_main_page(get_browser):
    AdminProjectsPage(get_browser).verify_project_page()


# T07: Admin fills in the billing details
@given("I get redirected to the billing page")
def redirect_to_billing_page(get_browser, alerts):
    AdminBillingPage(get_browser).redirect_to_billing()
    AdminBillingPage(get_browser).verify_billing_page()


@when(
    parsers.parse(
        "I fill the bill fields {firstname} {lastname} {cardnumber} {expiryyear} {expirymonth} {cvv} {country} {street} {city} {postal}"
    )
)
def fill_billing_details(
    get_browser,
    firstname,
    lastname,
    cardnumber,
    expiryyear,
    expirymonth,
    cvv,
    country,
    street,
    city,
    postal,
):
    # Handle environment variables for card details
    card_number = (
        os.getenv(cardnumber) if cardnumber.startswith("CARD_") else cardnumber
    )
    card_cvv = os.getenv(cvv) if cvv.startswith("CARD_") else cvv

    AdminBillingPage(get_browser).fill_bill(
        firstname,
        lastname,
        card_number,
        expiryyear,
        expirymonth,
        card_cvv,
        country,
        street,
        city,
        postal,
    )


@when("I click button to confirm the bill")
def click_confirm_button(get_browser):
    AdminBillingPage(get_browser).click_confirm_bill()


@then("I should see the card filled")
def verify_billing_success(get_browser):
    AdminBillingPage(get_browser).bill_success()


# T08: Admin fills the details of a new project and skips video
@given("I am at the create project page")
def navigate_to_create_project_page(get_browser):
    AdminProjectsPage(get_browser).create_new_project()


@when(parsers.parse('I fill the project fields {name} "{des}" {genre}'))
def fill_project_details(get_browser, name: str, des, genre):
    AdminProjectsPage(get_browser).fill_project(name, des, genre)


@when("I click project submit button")
def click_submit_button(get_browser):
    AdminProjectsPage(get_browser).submit_project()


@when("I skip the video upload")
def skip_video_upload(get_browser):
    AdminProjectsPage(get_browser).video_skip()


@then("I should see the project subscription page upon completion")
def verify_subscription_page(get_browser):
    AdminProjectsPage(get_browser).verify_sub_page()


# T09: Admin chooses a subscription model
@given("I am at the subscription page")
def navigate_to_subscription_page(get_browser):
    AdminSubscriptionPage(get_browser).navigate_sub_page()
    AdminSubscriptionPage(get_browser).verify_sub_page()


@when(parsers.parse('I choose subscription "{plan}"'))
def click_on_subscription_plan(get_browser, plan):
    plan_lower = plan.lower()
    if plan_lower == "trial":
        AdminSubscriptionPage(get_browser).click_trial()
    elif plan_lower == "premium plus":
        AdminSubscriptionPage(get_browser).click_premium()
    elif plan_lower == "high security":
        AdminSubscriptionPage(get_browser).click_high_security()
    elif plan_lower == "theatrical":
        AdminSubscriptionPage(get_browser).click_theatrical()


@when(parsers.parse('I confirm this subscription "{plan}"'))
def confirm_subscription_plan(get_browser, plan):
    plan_lower = plan.lower()
    if plan_lower == "premium plus":
        AdminSubscriptionPage(get_browser).click_confirm_pre()
    elif plan_lower == "high security":
        AdminSubscriptionPage(get_browser).click_confirm_high()
    elif plan_lower == "theatrical":
        AdminSubscriptionPage(get_browser).click_confirm_the()


@then("I should see the confirmation page")
def verify_confirmation_page(get_browser):
    AdminSubscriptionPage(get_browser).confirm_plan()


# T10: Admin uploads a video to the project
@given("I switch to project video page")
def navigate_to_video_page(get_browser):
    AdminVideoPage(get_browser).navigate_video_page()
    AdminVideoPage(get_browser).verify_video_page()


@when("I add video by clicking button")
def click_add_video_button(get_browser):
    AdminVideoPage(get_browser).click_on_new_video()


@when(
    parsers.parse(
        'I fill the video fields {name} {video} {roughcut} "{internalnotes}" {hi_res} {subtitle}'
    )
)
def fill_video_details(
    get_browser, name, video, roughcut: bool, internalnotes, hi_res, subtitle
):
    AdminVideoPage(get_browser).fill_video_form(
        name, video, roughcut, internalnotes, hi_res, subtitle
    )


@when("I click upload video button")
def click_upload_button(get_browser):
    AdminVideoPage(get_browser).click_upload()


@then("after uploading I should see the video watermark options")
def verify_video_watermark_options(get_browser):
    AdminVideoPage(get_browser).verify_upload()


# T11: Admin chooses the watermark option
@given("I am at the video watermark page")
def navigate_to_video_watermark_page():
    pass


@when(parsers.parse("I fill the watermark options {grid} {opacity} {freq}"))
def fill_watermark_options(get_browser, grid, opacity, freq):
    AdminVideoPage(get_browser).fill_watermark(opacity)


@when("I click on save video button")
def click_save_button(get_browser):
    AdminVideoPage(get_browser).click_save()


@then(parsers.parse("I should see video page with {video}"))
def verify_video_page_with_video(get_browser, video):
    AdminVideoPage(get_browser).upload_complete(video)
