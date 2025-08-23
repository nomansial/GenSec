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
      | 89ebd370-38bb-43e5-9956-5c8cda370b9c     | aae0a1b6-fafe-40af-ab20-87934343521f   |

  @Test
  Scenario Outline: Verify scan is initiated successfully with valid chatbot and environment IDs
    Given User sends POST request to initiate a scan with chatbot "<target_chatbot>" and environment "<target_env>"
    When the user receives the scan initiation response
    Then the status code returned should be 200 for successful scan initiation
    And the response should contain a "scan_id"
    And the response status should be "SCAN_REQUESTED"

    Examples:
      | target_chatbot                          | target_env                             |
      | 89ebd370-38bb-43e5-9956-5c8cda370b9c     | aae0a1b6-fafe-40af-ab20-87934343521f   |

  @Test
  Scenario Outline: Verify scan initiation fails when chatbot or environment is invalid
    Given User sends POST request to initiate a scan with chatbot "<target_chatbot>" and environment "<target_env>"
    When the user receives the scan initiation response
    Then the status code returned should be 404 for not found error
    And the response should contain an error message "Not Found"
    And the message should contain "Provided Chatbot <target_chatbot> not found in Environment <target_env>.Both chatbot and environment should exist and chatbot should be assigned to the environment."

    Examples:
      | target_chatbot                          | target_env                             |
      | 70ebd370-38bb-43e5-9956-5c8cda370b9c     | aae0a1b6-fafe-40af-ab20-87934343521f   |
      | 89ebd370-38bb-43e5-9956-5c8cda370b9c     | aae0a1b6-fafe-40af-ab20-87934343000f   |

  @Test
  Scenario: Verify scan initiation fails when chatbot and environment IDs are invalid format
    Given User sends POST request to initiate a scan with chatbot "invalid" and environment "invalid"
    When the user receives the scan initiation response
    Then the status code returned should be 400 for bad request error
    And the response should contain an error message "Bad Request"
    And the message should contain "Invalid input:"


