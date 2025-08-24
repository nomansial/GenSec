Feature: Get JSON Report by Scan ID using Genr3d API

  @Test
  Scenario Outline: Verify JSON report is returned correctly for a valid scan ID
    Given User sends GET request to fetch JSON report for scan ID "<scan_id>"
    When the user receives the JSON report response
    Then the status code returned should be 200 for successful report retrieval
    And chatboatname should contain a "chatbot_name"
    And the response should contain a valid "scan_id" matching "<scan_id>"
    And the response should contain a "start_timestamp" in ISO 8601 format
    And the response should contain an "end_timestamp" in ISO 8601 format
    And the response should contain a list of findings
    And each finding should contain:
      | name                |
      | description         |
      | attack_successful   |
      | severity            |
      | risk                |
      | mitigation          |
      | evidence            |
      | data_classification |
      | data_targeted       |

    Examples:
      | scan_id                                |
      | 3412a2c5-127b-476c-b399-af68ee4aefc7    |

