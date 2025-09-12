Feature: FireBase_Initiate Scan using Genr3d API

  @Test
  Scenario Outline: FireBase_Verify scan is initiated successfully with valid chatbot and environment IDs
    Given FireBase_User sends POST request to initiate a scan with chatbot "<target_chatbot>" and environment "<target_env>"
    When FireBase_the user receives the scan initiation response
    Then FireBase_the status code returned should be 200 for successful scan initiation
    And FireBase_the response should contain a "scan_id"
    And FireBase_the response status should be "SCAN_REQUESTED"

    Examples:
      | target_chatbot                          | target_env                             |
      | 3263adf3-94fb-43d3-b845-1c71ff37859f     | 68e8072f-4f3c-45b2-be48-e047c123820b   |

  @Test @Negative
  Scenario Outline: FireBase_Verify scan initiation fails when chatbot or environment is invalid
    Given FireBase_User sends POST request to initiate a scan with chatbot "<target_chatbot>" and environment "<target_env>"
    When FireBase_the user receives the scan initiation response
    Then FireBase_the status code returned should be 404 for not found error
    And FireBase_the response should contain an error message "Not Found"
    And FireBase_the message should contain "Provided Chatbot <target_chatbot> not found in Environment <target_env>.Both chatbot and environment should exist and chatbot should be assigned to the environment."

    Examples:
      | target_chatbot                          | target_env                             |
      | 70ebd370-38bb-43e5-9956-5c8cda370b1c     | aae0a1b6-fafe-40af-ab20-87934343521f   |

  @Test @Negative @Security
  Scenario: FireBase_Verify scan initiation fails when chatbot and environment IDs are invalid format
    Given FireBase_User sends POST request to initiate a scan with chatbot "invalid" and environment "invalid"
    When FireBase_the user receives the scan initiation response
    Then FireBase_the status code returned should be 400 for bad request error
    And FireBase_the response should contain an error message "Bad Request"
    And FireBase_the message should contain "Invalid input:"

