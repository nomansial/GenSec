Feature: FireBase_Verify Get Chatbot API


  @Test
  Scenario Outline: FireBase_Verify Get Chatbot API retrieves chatbots successfully for a given env_id
    Given FireBase_User sends GET request to fetch chatbots with env_id "<env_id>"
    When FireBase_the user receives the response
    Then FireBase_the status code returned should be 200 for a successful request
    And FireBase_the response should contain a "chatbots" array
    And FireBase_the "chatbots" array should contain at least one chatbot
    And FireBase_the response should contain chatbot details including "chatbot_id" and "name"

    Examples:
      | env_id                               |
      | f0b53f20-5ebe-4132-cbea-68725ef2c5c8 |

  @Test @Negative @Security
  Scenario Outline: FireBase_Verify Get Chatbot API when the env_id is invalid or missing
    Given FireBase_User sends GET request to fetch chatbots with env_id "<env_id>"
    When FireBase_the user receives the response
    Then FireBase_error code should be 400 for bad request error
    And FireBase_response shows error message "Bad Request"
    And FireBase_the message should be "Invalid input:"

    Examples:
      | env_id         |
      | asdf		   |
      | None           |
      | ' OR 1=1 --    |
      | <script>alert('XSS')</script> |
