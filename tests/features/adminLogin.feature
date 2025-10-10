Feature: SasS Admin login page
Covers the functionality of SaaS admin login

#  Background:
#    Given I navigate to the login page

  Scenario Outline: Admin verifies that the login website is correct
    Given I navigate to the login page
    When I check the page title
    Then I should see the correct <TITLE>
    Examples:
      | TITLE             |
      | Indee Login Page  |

    Scenario Outline: Sign up a new admin account
      Given I navigate to the login page
      When I click on the Sign up link
      And I fill the fields <EMAIL> <PASSWORD> <CONFIRMPASSWORD> <FIRSTNAME> <LASTNAME> <COMPANYNAME> on SignUp Page
      And I click on the SignUp button
      Then I should see the success message
      Examples:
        | EMAIL         | PASSWORD  | CONFIRMPASSWORD | FIRSTNAME | LASTNAME | COMPANYNAME |
        | temp@fake.com | Fake432!  | Fake432!        | clifford  | temp     | fake        |

    Scenario Outline: User verifies their new account through mail
      Given I open the nimad page
      When I log into the <ACCOUNT> and <PASSWORD>
      And I navigate to the email list
      Then I should see the <EMAIL> initiated
      Examples:
        | ACCOUNT   | PASSWORD  | EMAIL         |
        | nimad_acc | nimad_key | temp@fake.com |

    Scenario Outline: Admin signs into the login page with valid credentials
      When I fill the valid <EMAIL> and <PASSWORD>
      And I click on the login button
      Then I should see the main page
      Examples:
        | EMAIL                 | PASSWORD          |
        | clifford-the@indee.tv | Theatrical!111    |

    @negative
    Scenario Outline: Admin signs into the login page with invalid credentials
      When I fill the invalid <EMAIL> and <PASSWORD>
      And I click on the login button
      Then I should see an error message as failure
      Examples:
        | EMAIL            | PASSWORD          |
        | invalid@indee.tv | invalid-password  |
