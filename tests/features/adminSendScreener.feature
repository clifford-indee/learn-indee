Feature: SaaS Admin creates a new Screener room and sends it


  # Use .env for NIMAD url, account and password
  Scenario Outline: T12: Admin receives email that the video transcoding is complete
    Given I open nimad <NIMAD> page
    When I login using nimad <ACCOUNT> and <PASSWORD>
    And I navigate to the email list
    Then I should receive the video encoding completion email for <EMAIL>
    Examples:
      | NIMAD        | ACCOUNT   | PASSWORD  | EMAIL               |
      | PUNIQA_NIMAD | NIMAD_ACC | NIMAD_KEY | test_cliff@fake.com |
      #| PUNIQA_NIMAD | NIMAD_ACC | NIMAD_KEY | ACC_PRE             | sample email

  # Use .env keys for EMAIL and PASSWORD
  @T13
  Scenario Outline: T13: Admin signs into the login page with valid credentials
    Given I navigate to screeners <LOGIN> page
    When I fill account <EMAIL> and <PASSWORD> for screeners
    And I click to submit login
    Then I should see landing project page
    Examples:
      | LOGIN      | EMAIL               | PASSWORD    |
      | PUNIQA_URL | test_cliff@fake.com | Autorun432! |
      #| PUNIQA_URL | ACC_PRE             | KEY_PRE     | sample account

  # Use .env for NIMAD url, account and password
  @T14
  Scenario Outline: T14: Admin searches for the project and navigates to it
    Given I am at the projects page
    When I use search bar for project <PROJECT:s>
    And I click on the first result project
    Then I should get redirected to the project's video page
    Examples:
      | PROJECT:s   |
      | auto-proj{} |
      #| auto-proj86 | sample project

  # Watermark: None, Overlay, Forensic, Burned and Security: None, Password, 2FA
  Scenario Outline: T15: Admin sends a screener room via email
    Given I am on the send screener page
    When I choose all videos
    And I fill the screener fields <VIEWS> <STARTDATE> <STARTTIME> <ENDDATE> <ENDTIME> <SECURITY> <WATERMARKTYPE> for email
    And I click on screener continue button
    And I fill the recipient fields <EMAIL> <WATERMARK:s> <NAME>
    And I click on send email button to screener
    Then I should see screener result page with the correct email
    Examples:
      | VIEWS | STARTDATE  | STARTTIME | ENDDATE    | ENDTIME  | SECURITY | WATERMARKTYPE | EMAIL             | WATERMARK:s | NAME     |
      | 10    | 2025-10-14 | 20:00:00  | 2025-11-14 | 20:00:00 | None     | Overlay       | clifford@indee.tv | testrun{}   | clifford |

  Scenario Outline: T16: Admin confirms the screener room is sent
    Given I sent a screener room
    And I switch to the Screeners room tab
    When I search the screener room list for <RECIPIENT:s>
    Then I should see result screener room
    Examples:
      | RECIPIENT:s |
      | clifford@indee.tv|

  Scenario Outline: T17: User receives the screener email
    Given I open nimad <NIMAD> page
    And I am already logged in nimad
    When I navigate to the email list
    Then I should see that the user <EMAIL> received the screener email
    Examples:
      | NIMAD        | EMAIL             |
      | PUNIQA_NIMAD | clifford@indee.tv |
