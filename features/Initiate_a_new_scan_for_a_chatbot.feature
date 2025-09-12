Feature: Initiate Scan using Genr3d API

  @Test
  Scenario Outline: Verify scan is initiated successfully with valid chatbot and environment IDs
    Given User sends POST request to initiate a scan with chatbot "<target_chatbot>" and environment "<target_env>"
    When the user receives the scan initiation response
    Then the status code returned should be 200 for successful scan initiation
    And the response should contain a "scan_id"
    And the response status should be "SCAN_REQUESTED"

    Examples:
      | target_chatbot                          | target_env                             |
      | 20b49f8a-6591-4081-af50-d542e9a0914e     | bdacf6f7-9499-478a-9b05-f1966f25f389   |

  @Test @Negative
  Scenario Outline: Verify scan initiation fails when chatbot or environment is invalid
    Given User sends POST request to initiate a scan with chatbot "<target_chatbot>" and environment "<target_env>"
    When the user receives the scan initiation response
    Then the status code returned should be 404 for not found error
    And the response should contain an error message "Not Found"
    And the message should contain "Provided Chatbot <target_chatbot> not found in Environment <target_env>.Both chatbot and environment should exist and chatbot should be assigned to the environment."

    Examples:
      | target_chatbot                          | target_env                             |
      | 70ebd370-38bb-43e5-9956-5c8cda370b1c     | aae0a1b6-fafe-40af-ab20-87934343521f   |

  @Test @Negative @Security
  Scenario: Verify scan initiation fails when chatbot and environment IDs are invalid format
    Given User sends POST request to initiate a scan with chatbot "invalid" and environment "invalid"
    When the user receives the scan initiation response
    Then the status code returned should be 400 for bad request error
    And the response should contain an error message "Bad Request"
    And the message should contain "Invalid input:"

