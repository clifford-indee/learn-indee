Feature: SasS Admin login page
Covers the functionality of SaaS admin login

#  Background:
#    Given I navigate to the login page

  # Use the .env key for LOGIN url
  Scenario Outline: T01: Admin verifies that the login website is correct
    Given I navigate to the <LOGIN> page
    When I check the page title
    Then I should see the correct title
    Examples:
      | LOGIN      |
      | PUNIQA_URL |

  Scenario Outline: T02: Sign up a new admin account
      Given I navigate to the login page
      When I click on the Sign up link
      And I fill the fields <EMAIL> <PASSWORD> <CONFIRMPASSWORD> <FIRSTNAME> <LASTNAME> <COMPANYNAME> on SignUp Page
      And I click on the SignUp button
      Then I should see the success message
      Examples:
        | EMAIL         | PASSWORD  | CONFIRMPASSWORD | FIRSTNAME | LASTNAME | COMPANYNAME |
        | temp@fake.com | Fake432!  | Fake432!        | clifford  | temp     | fake        |

    # Use .env keys for NIMAD url, account and password
    Scenario Outline: T03: User verifies their new account through mail
      Given I open the <NIMAD> page
      When I log into the <ACCOUNT> and <PASSWORD>
      And I navigate to the email list
      Then I should see the <EMAIL> has been initiated
      Examples:
        | NIMAD        | ACCOUNT   | PASSWORD  | EMAIL         |
        | PUNIQA_NIMAD | NIMAD_ACC | NIMAD_KEY | temp@fake.com |

    # Use .env keys for EMAIL and PASSWORD
    Scenario Outline: T04: Admin signs into the login page with valid credentials
      When I fill the valid <EMAIL> and <PASSWORD>
      And I click on the login button
      Then I should see the main page
      Examples:
        | EMAIL   | PASSWORD |
        | ACC_THE | THE_KEY  |

    @negative
    Scenario Outline: T05: Admin signs into the login page with invalid credentials
      When I fill the invalid <EMAIL> and <PASSWORD>
      And I click on the login button
      Then I should see an error message as failure
      Examples:
        | EMAIL            | PASSWORD          |
        | invalid@indee.tv | invalid-password  |
