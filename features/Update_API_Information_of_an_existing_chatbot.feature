Feature: Update Chatbot API Details using Genr3d API

  @Test
  Scenario Outline: Validate successful update of chatbot API details
    Given User sends PUT request to update chatbot API details for chatbot ID with environment ID and endpoint "<chatbot_url>"
    When the user receives the chatbot API update response
    Then the status code returned should be 200 for successful update
    And the response should contain a valid chatbotID
    And the response should contain a "status" equal to "API_updated"

    Examples:
      | chatbot_url                          |
      | http://34.36.66.146/stream_messages  |

  @Test
  Scenario Outline: Validate chatbot API update response when chatbot ID is not found
    Given User sends PUT request to update chatbot API details for chatbot ID "<chatbot_id>" with environment ID "<env_id>" and endpoint "<chatbot_url>"
    When the user receives the chatbot API update response
    Then should be 404 for not found error
    And should error message "Not Found"
    And the message should contain "Chatbot with ID <chatbot_id> not found."

    Examples:
      | chatbot_id                             | env_id                                 | chatbot_url                          |
      | 89ebd370-38bb-43e5-9956-5c8cda370b8c    | aae0a1b6-fafe-40af-ab20-87934343521f   | http://34.36.66.146/stream_messages  |


