Feature: FireBase_Update Chatbot API


  @Test
  Scenario Outline: FireBase_Verify PUT request successfully updates chatbot details
    Given FireBase_User sends PUT request to update chatbot details with chatbot_name "<chatbot_name>", chatbot_description "<chatbot_description>", and env_id "<env_id>"
    When FireBase_the user receives the response
    Then FireBase_the status code returned should be 200 for a successful request
    And FireBase_the response should contain the chatbot_id
    And FireBase_the status should be In_progress

    Examples:
      | chatbot_name     | chatbot_description              | env_id                               |
     | New updated Name | Updated through Automation suite | f0b53f20-5ebe-4132-cbea-68725ef2c5c8 |

  @Test @Negative
  Scenario Outline: FireBase_Negative Verify PUT request successfully updates chatbot details
    Given FireBase_User sends PUT request to update chatbot details with chatbot_id "<chatbot_id>", chatbot_name "<chatbot_name>", chatbot_description "<chatbot_description>", and env_id "<env_id>"
    When FireBase_the user receives the response
    Then FireBase_the status code returned should be 400
    And FireBase_the response should contain error variable with value Bad Request
    And FireBase_the response should contain the The chatbot must be in AVAILABLE status

    Examples:
      | chatbot_id                           | chatbot_name     | chatbot_description              | env_id                               |
      | a4bdb755-64bb-4fa8-a35e-209810c70bda | New updated Name | Updated through Automation suite | f0b53f20-5ebe-4132-cbea-68725ef2c5c8 |

  @Test @Security
  Scenario Outline: FireBase_SQL Injection Attempt in PUT request for chatbot details
    Given FireBase_User sends request with chatbot_id "<chatbot_id>", chatbot_name "<chatbot_name>", chatbot_description "<chatbot_description>", and env_id "<env_id>"
    When FireBase_the user receives the response
    Then  FireBase_the response should contain error variable The current request is matched to the defined
    And FireBase_the response should contain invalid input message

    Examples:
      | chatbot_id   | chatbot_name    | chatbot_description | env_id       |
      | ' OR 1=1 --  | ' OR 1=1 --      | ' OR 1=1 --          | ' OR 1=1 -- |