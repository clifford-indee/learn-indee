Feature: SasS Admin login page
Covers the functionality of SaaS admin login

  # Use the .env key for LOGIN url
  Scenario Outline: T01: Admin verifies that the login website is correct
    Given I navigate to the <LOGIN> page
    When I check the page title
    Then I should see the correct title
    Examples:
      | LOGIN      |
      | PUNIQA_URL |

  Scenario Outline: T02: Sign up a new admin account
    Given I navigate to the <LOGIN> page
    When I click on the Sign up link
    And I fill the fields <EMAIL> <PASSWORD> <FIRSTNAME> <LASTNAME> <COMPANYNAME> on SignUp Page
    And I click on the SignUp button
    Then I should see the success message
      Examples:
        | LOGIN      | EMAIL               | PASSWORD  | FIRSTNAME | LASTNAME | COMPANYNAME |
        | PUNIQA_URL | test_cliff@fake.com | Temp432!  | clifford  | temp     | fake        |

    # Use .env keys for NIMAD url, account and password
    Scenario Outline: T03: User verifies their new account through mail
      Given I open the <NIMAD> page
      When I log into the <ACCOUNT> and <PASSWORD>
      And I navigate to the email list
      Then I should see the <EMAIL> has been initiated
      Examples:
        | NIMAD        | ACCOUNT   | PASSWORD  | EMAIL               |
        | PUNIQA_NIMAD | NIMAD_ACC | NIMAD_KEY | test_cliff@fake.com |

    # Use .env keys for EMAIL and PASSWORD
    Scenario Outline: T04: Admin signs into the login page with valid credentials
      Given I navigate to the <LOGIN> page
      When I fill the valid <EMAIL> and <PASSWORD>
      And I click on the login button
      Then I should see the main page and log out <EMAIL>
      Examples:
        | LOGIN      | EMAIL   | PASSWORD |
        | PUNIQA_URL | ACC_PRE | KEY_PRE  |

    @negative
    Scenario Outline: T05: Admin signs into the login page with invalid credentials
      Given I navigate to the <LOGIN> page
      When I fill the invalid <EMAIL> and <PASSWORD>
      And I click on the login button
      Then I should see an error message as failure
      Examples:
        | LOGIN      | EMAIL            | PASSWORD          |
        | PUNIQA_URL | invalid@indee.tv | invalid-password  |
