Feature: FireBase_Update Chatbot API Details using Genr3d API

  @Test
  Scenario Outline: FireBase_Validate successful update of chatbot API details
    Given FireBase_User sends PUT request to update chatbot API details for chatbot ID with environment ID and endpoint "<chatbot_url>"
    When FireBase_the user receives the chatbot API update response
    Then FireBase_the status code returned should be 200 for successful update
    And FireBase_the response should contain a valid chatbotID
    And FireBase_the response should contain a "status" equal to "API_updated"

    Examples:
      | chatbot_url                          |
      | http://34.36.66.146/stream_messages  |

  @Test @Negative
  Scenario Outline: FireBase_Validate chatbot API update response when chatbot ID is not found
    Given FireBase_User sends PUT request to update chatbot API details for chatbot ID "<chatbot_id>" with environment ID "<env_id>" and endpoint "<chatbot_url>"
    When FireBase_the user receives the chatbot API update response
    Then FireBase_should be 404 for not found error
    And FireBase_should error message "Not Found"
    And FireBase_the message should contain "Chatbot with ID <chatbot_id> not found."

    Examples:
      | chatbot_id                             | env_id                                 | chatbot_url                          |
      | 89ebd370-38bb-43e5-9956-5c8cda370b8c    | aae0a1b6-fafe-40af-ab20-87934343521f   | http://34.36.66.146/stream_messages  |


  @Test @Security
  Scenario Outline: FireBase_SQL injection attempt in the Update Chatbot API request
    Given FireBase_User send request to update API "<chatbot_id>" with environment ID "<env_id>" and endpoint "<chatbot_url>"
    When FireBase_the user receives the API response
    Then FireBase_message should contain "Invalid input:"
    And FireBase_the message should contain "chatbot_id" with validation errors related to the input

    Examples:
      | chatbot_id           | env_id               | chatbot_url               |
      | ' OR 1=1 --          | ' OR 1=1 --          | ' OR 1=1 --               |

