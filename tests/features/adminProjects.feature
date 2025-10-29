Feature: SaaS Admin creates new project titles and it's respective content


  @T06
  Scenario Outline: T06: Admin login to their project account
    Given I navigate to project <LOGIN>
    When I enter project account <EMAIL> and <PASSWORD>
    And I submit the login form
    Then I should see the main page
    Examples:
      | LOGIN      | EMAIL               | PASSWORD    |
      | PUNIQA_URL | test_cliff@fake.com | Autorun432! |


  @T07
  # CARD_NUM and CARD_CVV are .env keys
  Scenario Outline: T07: Admin fills in the billing details
    Given I get redirected to the billing page
    When I fill the bill fields <FIRSTNAME> <LASTNAME> <CARDNUMBER> <EXPIRYYEAR> <EXPIRYMONTH> <CVV> <COUNTRY> <STREET> <CITY> <POSTAL>
    And I click button to confirm the bill
    Then I should see the card filled
    Examples:
      | FIRSTNAME | LASTNAME | CARDNUMBER | EXPIRYYEAR | EXPIRYMONTH | CVV      | COUNTRY | STREET | CITY | POSTAL |
      | auto      | run      | CARD_NUM   | 2026       | 01-January  | CARD_CVV | India   | street | city | 123456 |


  @T08
  Scenario Outline: T08: Admin fills the details of a new project and skips video
    Given I am at the create project page
    When I fill the project fields <NAME> "<DESCRIPTION>" <GENRE>
    And I click project submit button
    And I skip the video upload
    Then I should see the project subscription page upon completion
    Examples:
      | NAME        | DESCRIPTION   | GENRE |
      | auto-proj{} | Framework run | Anime |


  @T09
  # "Trial", "Premium plus", "High Security" or "Theatrical"
  Scenario Outline: T09: Admin chooses a subscription model
    Given I am at the subscription page
    When I choose subscription "<PLAN>"
    And I confirm this subscription "<PLAN>"
    Then I should see the confirmation page
    Examples:
      | PLAN          |
      | Premium plus  |


  @T10
  # Files names from the sample directory
  Scenario Outline: T10: Admin uploads a video to the project
    Given I switch to project video page
    When I add video by clicking button
    And I fill the video fields <NAME> <VIDEO> <ROUGHCUT:b> "<INTERNALNOTES>" <HI_RES> <SUBTITLE>
    And I click upload video button
    Then after uploading I should see the video watermark options
    Examples:
      | NAME       | VIDEO                  | ROUGHCUT:b | INTERNALNOTES        | HI_RES     | SUBTITLE     |
      | test_video | 1080p-60fps-30sec.mp4  | True       | Automation run video | banner.jpg | subtitle.vtt |


  @T11
  #
  Scenario Outline: T11: Admin chooses the watermark option
    Given I am at the video watermark page
    When I fill the watermark options <GRID> <OPACITY> <FREQUENCY>
    And I click on save video button
    Then I should see video page with <VIDEO>
    Examples:
      | GRID | OPACITY | FREQUENCY | VIDEO      |
      | 11   | 80      | Always    | test_video |
