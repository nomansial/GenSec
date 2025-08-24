Feature: Get Scans by Chatbot ID using Genr3d API

  @Test
  Scenario Outline: Verify scans are returned correctly for a valid chatbot ID
    Given User sends GET request to fetch scans for chatbot ID "<chatbot_id>"
    When the user receives the scans response
    Then the status code returned should be 200 for successful scans retrieval
    And the response should contain a list of scans
    And each scan should contain a valid "scan_id" of length 36
    And each scan should contain a "creation_timestamp" in ISO 8601 format
    And each scan should have a "status" equal to "REPORT_GENERATED"

    Examples:
      | chatbot_id                              |
      | 89ebd370-38bb-43e5-9956-5c8cda370b9c     |

  @Test
  Scenario Outline: Verify scans API returns empty list for invalid chatbot ID
    Given User sends GET request to fetch scans for chatbot ID "<chatbot_id>"
    When the user receives the scans response
    Then the status code returned should be 200 for successful scans retrieval
    And the response should contain an empty list of scans

    Examples:
      | chatbot_id                              |
      | 89ebd370-38bb-43e5-9956-5c8cda370b90     |

  @Test
  Scenario Outline: Verify scans API returns 400 for invalid chatbot ID format
    Given User sends GET request to fetch scans for chatbot ID "<chatbot_id>"
    When the user receives the scans response
    Then the status code returned should be 400 for bad request error
    And the response should contain an error message "Bad Request"
    And the message should contain "Invalid input:"

    Examples:
      | chatbot_id   |
      | invalid      |


