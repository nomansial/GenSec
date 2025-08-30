Feature: Create Chatbot API

  @Test @positive
  Scenario: Verify Create Chatbot API creates a chatbot successfully
    Given User sends POST request to create a chatbot with valid details
    When the user receives the response
    Then the status code returned should be 200 for the created chatbot
    And the response should contain a "chatbot_id"

  @Test @Negative
  Scenario Outline: Verify Create Chatbot API when the chatbot name is invalid (Negative Case)
    Given User sends POST request to create a chatbot with an invalid chatbot name "<chatbot_name>"
    When the user receives the response
    Then the status code should be 400 for bad request error
    And the response should contain an error message "Bad Request"
    And the message should contain "Invalid input:"

    Examples:
      | chatbot_name |
      | None         |

  @Test
  Scenario Outline: Verify Create Chatbot API when required fields are missing (Negative Case)
    Given User sends POST request to create a chatbot with missing required fields "<field>"
    When the user receives the response
    Then the status code should be 400 for bad request error
    And the response should contain an error message "Bad Request"
    And the message should contain "Invalid input:"

    Examples:
      | field              |
      | env_id             |
      | chatbot_name       |
      | api_endpoint       |
      | api_secret         |
      | chatbot_url        |
      | chatbot_description |