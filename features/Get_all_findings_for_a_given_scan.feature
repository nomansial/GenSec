Feature: Get Findings by Scan ID using Genr3d API

  @Test
  Scenario Outline: Validate findings response for a valid scan ID
    Given User sends GET request to fetch findings for scan ID "<scan_id>"
    When the user receives the findings response
    Then the status code returned should be 200 for successful findings retrieval
    And the response should contain a valid "chatbot_id" of length 36
    And the response should contain a non-empty "chatbot_name"
    And the "scan_id" in response should match "<scan_id>"
    And the response should contain a non-empty list of findings
    And each finding should include the following fields:
      | finding_id         |
      | finding_name       |
      | attack_successful  |
      | creation_timestamp |
      | severity           |
      | risk               |
    And each finding with a "creation_timestamp" should be in ISO 8601 format

    Examples:
      | scan_id                                |
      | 3412a2c5-127b-476c-b399-af68ee4aefc7    |

  @Test @Negative
  Scenario Outline: Validate findings response when scan ID is not found
    Given User sends GET request to fetch findings for scan ID "<scan_id>"
    When the user receives the findings response
    Then the status code returned should be 200 for successful findings retrieval
    And the response should contain null "chatbot_id" and "chatbot_name"
    And the "scan_id" in response should match "<scan_id>"
    And the response should contain an empty list of findings

    Examples:
      | scan_id                                |
      | 3412a2c5-127b-476c-b399-af68ee4aef00    |

  @Test @Negative
  Scenario Outline: Validate findings response for invalid scan ID format
    Given User sends GET request to fetch findings for scan ID "<scan_id>"
    When the user receives the findings response
    Then the status code returned should be 400 for bad request error
    And the response should contain an error message "Bad Request"
    And the message should contain "Invalid input:"

    Examples:
      | scan_id   |
      | invalid   |
      |' OR 1=1 --|
      | <script>alert('XSS')</script> |
