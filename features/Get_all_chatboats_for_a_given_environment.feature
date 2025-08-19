Feature: Verify Get Chatbot API


  @Test
  Scenario Outline: Verify Get Chatbot API retrieves chatbots successfully for a given env_id
    Given User sends GET request to fetch chatbots with env_id "<env_id>"
    When the user receives the response
    Then the status code returned should be 200 for a successful request
    And the response should contain a "chatbots" array
    And the "chatbots" array should contain at least one chatbot
    And the response should contain chatbot details including "chatbot_id" and "name"

    Examples:
      | env_id                               |
      | f0b53f20-5ebe-4132-cbea-68725ef2c5c8 |

  @Test
  Scenario Outline: Verify Get Chatbot API when the env_id is invalid or missing
    Given User sends GET request to fetch chatbots with env_id "<env_id>"
    When the user receives the response
    Then error code should be 400 for bad request error
    And response shows error message "Bad Request"
    And the message should be "Invalid input:"

    Examples:
      | env_id         |
      | asdf		   |
      | None           |
