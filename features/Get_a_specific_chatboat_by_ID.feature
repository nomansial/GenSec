Feature: Verify Get Chatbot API

  @Test
  Scenario Outline: Verify Get Chatbot API returns "Not Found" for a valid chatbot_id but non-existing chatbot
    Given User sends GET request to fetch chatbot details with chatbot_id "<chatbot_id>"
    When the user receives the response
    Then the status code returned should be 404 for "Not Found"
    And the error message should state Chatbot with ID not found.

    Examples:
      | chatbot_id                                 |
      | d8d4c7b6-a4a4-4839-94d5-da4bb139043f       |

    @Test
  Scenario Outline: Verify Get Chatbot API retrieves chatbot details successfully for a given chatbot_id
    Given User sends GET request to fetch chatbot details with chatbot_id "<chatbot_id>"
    When the user receives the response
    Then the status code returned should be 200 for a successful request
    And the response should contain the chatbot details
    And all the parameters in the response should not be None except for api_specifications

    Examples:
      | chatbot_id                                 |
      | 246b839f-77c3-48e5-b8d2-7e4762d8a09b       |

  @Test
  Scenario Outline: Verify Get Chatbot API returns error for an invalid chatbot_id
    Given User sends GET request to fetch chatbot details with chatbot_id "<chatbot_id>"
    When the user receives the response
    Then the status code returned should be 400 for a bad request
    And the response should contain an error message
    And the error message should state "Invalid input" with a specific message for chatbot_id

    Examples:
      | chatbot_id             |
      | asdfasdfasdfsadf       |