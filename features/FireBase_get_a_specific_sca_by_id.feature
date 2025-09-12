
Feature: FireBase_Get Scan Details using Genr3d API


  @Test
  Scenario Outline: FireBase_Verify scan details are returned correctly for a valid scan ID
    Given FireBase_User sends GET request to fetch scan details for scan ID "<scan_id>"
    When FireBase_the user receives the scan details response
    Then FireBase_the status code returned should be 200 for successful scan details retrieval
    And FireBase_the response should contain a valid "chatbot_id" of length 36
    And FireBase_the response should contain a "chatbot_name"
    And FireBase_the "creation_timestamp" should be in ISO 8601 format
    And FireBase_the "last_update_timestamp" should be in ISO 8601 format
    And FireBase_the "scan_id" should match the requested scan ID "<scan_id>"
    And FireBase_the "status" should be "SCAN_COMPLETED"

    Examples:
      | scan_id                                |
      | 66a3519e-8f94-43da-8be3-052ec1f5727f    |


  @Test @Negative
  Scenario Outline: FireBase_Verify scan details API returns 404 when scan ID is not found
    Given FireBase_User sends GET request to fetch scan details for scan ID "<scan_id>"
    When FireBase_the user receives the scan details response
    Then FireBase_the status code returned should be 404 for not found error
    And FireBase_the response should contain an error message "Not Found"
    And FireBase_the message should contain "Scan with ID <scan_id> not found."

    Examples:
      | scan_id                                |
      | 66a3519e-8f94-43da-8be3-052ec1f57200    |

  @Test @Negative @Security
  Scenario Outline: FireBase_Verify scan details API returns 400 for invalid scan ID format
    Given FireBase_User sends GET request to fetch scan details for scan ID "<scan_id>"
    When FireBase_the user receives the scan details response
    Then FireBase_the status code returned should be 400 for bad request error
    And FireBase_the response should contain an error message "Bad Request"
    And FireBase_the message should contain "Invalid input:"

    Examples:
      | scan_id     |
      | invalid     |
      | ' OR 1=1 -- |

  @Test @Security
  Scenario: FireBase_XSS injection attempt in finding ID "<script>alert('XSS');</script>"
    Given FireBase_Specific Scan by ID the user sends GET request with finding ID
    When FireBase_the user receives the response
    Then FireBase_Specific Scan by ID the status code returned should be 404
    And FireBase_Specific Scan by ID the message should contain "The current request is not defined by this API."


