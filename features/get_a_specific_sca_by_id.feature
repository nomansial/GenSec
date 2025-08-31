
Feature: Get Scan Details using Genr3d API


  @Test
  Scenario Outline: Verify scan details are returned correctly for a valid scan ID
    Given User sends GET request to fetch scan details for scan ID "<scan_id>"
    When the user receives the scan details response
    Then the status code returned should be 200 for successful scan details retrieval
    And the response should contain a valid "chatbot_id" of length 36
    And the response should contain a "chatbot_name"
    And the "creation_timestamp" should be in ISO 8601 format
    And the "last_update_timestamp" should be in ISO 8601 format
    And the "scan_id" should match the requested scan ID "<scan_id>"
    And the "status" should be "SCAN_COMPLETED"

    Examples:
      | scan_id                                |
      | 66a3519e-8f94-43da-8be3-052ec1f5727f    |


  @Test @Negative
  Scenario Outline: Verify scan details API returns 404 when scan ID is not found
    Given User sends GET request to fetch scan details for scan ID "<scan_id>"
    When the user receives the scan details response
    Then the status code returned should be 404 for not found error
    And the response should contain an error message "Not Found"
    And the message should contain "Scan with ID <scan_id> not found."

    Examples:
      | scan_id                                |
      | 66a3519e-8f94-43da-8be3-052ec1f57200    |

  @Test @Negative @Security
  Scenario Outline: Verify scan details API returns 400 for invalid scan ID format
    Given User sends GET request to fetch scan details for scan ID "<scan_id>"
    When the user receives the scan details response
    Then the status code returned should be 400 for bad request error
    And the response should contain an error message "Bad Request"
    And the message should contain "Invalid input:"

    Examples:
      | scan_id     |
      | invalid     |
      | ' OR 1=1 -- |

  @Test @Security
  Scenario: XSS injection attempt in finding ID "<script>alert('XSS');</script>"
    Given Specific Scan by ID the user sends GET request with finding ID
    When the user receives the response
    Then Specific Scan by ID the status code returned should be 404
    And Specific Scan by ID the message should contain "The current request is not defined by this API."


