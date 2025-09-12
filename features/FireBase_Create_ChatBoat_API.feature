Feature: FireBase_Create Chatbot API

  @Test
  Scenario: FireBase_Verify Create Chatbot API creates a chatbot successfully
    Given Firebase_User sends POST request to create a chatbot with valid details
    When Firebase_the user receives the response
    Then Firebase_the status code returned should be 200 for the created chatbot
    And Firebase_the response should contain a "chatbot_id"

  @Test @Negative
  Scenario Outline: FireBase_Verify Create Chatbot API when the chatbot name is invalid (Negative Case)
    Given Firebase_User sends POST request to create a chatbot with an invalid chatbot name "<chatbot_name>"
    When Firebase_the user receives the response
    Then Firebase_the status code should be 400 for bad request error
    And Firebase_the response should contain an error message "Bad Request"
    And Firebase_the message should contain "Invalid input:"

    Examples:
      | chatbot_name |
      | None         |

  @Test @Negative
  Scenario Outline: FireBase_Verify Create Chatbot API when required fields are missing (Negative Case)
    Given Firebase_User sends POST request to create a chatbot with missing required fields "<field>"
    When Firebase_the user receives the response
    Then Firebase_the status code should be 400 for bad request error
    And Firebase_the response should contain an error message "Bad Request"
    And Firebase_the message should contain "Invalid input:"

    Examples:
      | field               |
      | env_id              |
      | chatbot_name        |
      | api_endpoint        |
      | api_secret          |
      | chatbot_url         |
      | chatbot_description |

  @Test @Security
  Scenario Outline: FireBase_SQL injection attempt in input fields
    Given Firebase_User sends POST request with "<field>" containing SQL injection "' OR 1=1 --"
    When Firebase_the user receives the response
    Then Firebase_the response should contain the message "Invalid input:"

    Examples:
      | field               |
      | env_id              |
      | chatbot_name        |
      | api_endpoint        |
      | api_secret          |
      | chatbot_url         |
      | chatbot_description |

  @Test @Security
  Scenario Outline: FireBase_Cross-Site Scripting (XSS) attempt in input fields
    Given Firebase_User sends POST request with "<field>" containing "<script>alert('XSS')</script>"
    When Firebase_the user receives the response
    Then Firebase_the response should contain the message "Invalid input:"

    Examples:
      | field               |
      | env_id              |
      | chatbot_name        |
      | api_endpoint        |
      | api_secret          |
      | chatbot_url         |
      | chatbot_description |
