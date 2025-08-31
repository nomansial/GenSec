Feature: Fetch Environment Details API

  @Test
  Scenario: Verify Fetch Environment Details API for a successful request (Positive Case)
    Given take env_id from Create Environment API
    When user sends GET request to fetch environment details with valid env_id
    Then the status code should be 200 for the successful request
    And the response should contain the env_id
    And the "creation_timestamp" should be in the correct timestamp format (yyyy-MM-dd'T'HH:mm:ss'Z')
    And the "last_update_timestamp" should be in the correct timestamp format (yyyy-MM-dd'T'HH:mm:ss'Z')
    And the "description" should not be null
    And the "name" should not be null
    And the "env_id" should match the env_id fetched from Create Environment API

  @Test @Negative @Security
  Scenario Outline: Verify Fetch Environment Details API when environment is not found (Negative Case)
    Given User sends GET request to fetch environment details with an invalid or missing env_id "<env_id>"
    When user receives the response
    Then the status code should be 400 for not found error
    And the response should contain an error message

  Examples:
    | env_id                            |
    | ab809075-108f-4f67-2fb5-asdf      |
    | None                              |
    | ' OR 1=1 --                       |

  @Test @Security
  Scenario Outline: Verify API should return error message when XSS injection is passed in env_id
    Given User sends GET request to fetch environment details with an invalid env_id "<env_id>"
    When user receives the response
    Then API should contain the message Current request is not defined by this API

  Examples:
    | env_id                            |
    | <script>alert('XSS')</script>     |