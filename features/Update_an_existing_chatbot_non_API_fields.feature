Feature: Update Chatbot API

  @Test
  Scenario Outline: Verify PUT request successfully updates chatbot details
    Given User sends PUT request to update chatbot details with chatbot_name "<chatbot_name>", chatbot_description "<chatbot_description>", and env_id "<env_id>"
    When the user receives the response
    Then the status code returned should be 200 for a successful request
    And the response should contain the chatbot_id
    And the status should be In_progress

    Examples:
      | chatbot_name     | chatbot_description              | env_id                               |
     | New updated Name | Updated through Automation suite | f0b53f20-5ebe-4132-cbea-68725ef2c5c8 |

  @Test
  Scenario Outline: Negative Verify PUT request successfully updates chatbot details
    Given User sends PUT request to update chatbot details with chatbot_id "<chatbot_id>", chatbot_name "<chatbot_name>", chatbot_description "<chatbot_description>", and env_id "<env_id>"
    When the user receives the response
    Then the status code returned should be 400
    And the response should contain error variable with value Bad Request
    And the response should contain the The chatbot must be in AVAILABLE status

    Examples:
      | chatbot_id                           | chatbot_name     | chatbot_description              | env_id                               |
      | a4bdb755-64bb-4fa8-a35e-209810c70bda | New updated Name | Updated through Automation suite | f0b53f20-5ebe-4132-cbea-68725ef2c5c8 |