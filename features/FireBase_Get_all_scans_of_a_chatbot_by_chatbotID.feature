Feature: FireBase_Get Scans by Chatbot ID using Genr3d API

  @Test
  Scenario Outline: FireBase_Verify scans are returned correctly for a valid chatbot ID
    Given FireBase_User sends GET request to fetch scans for chatbot ID "<chatbot_id>"
    When FireBase_the user receives the scans response
    Then FireBase_the status code returned should be 200 for successful scans retrieval
    And FireBase_the response should contain a list of scans
    And FireBase_each scan should contain a valid "scan_id" of length 36
    And FireBase_each scan should contain a "creation_timestamp" in ISO 8601 format
    And FireBase_each scan should have a "status" equal to "REPORT_GENERATED"

    Examples:
      | chatbot_id                              |
      | 89ebd370-38bb-43e5-9956-5c8cda370b9c     |

  @Test @Negative
  Scenario Outline: FireBase_Verify scans API returns empty list for invalid chatbot ID
    Given FireBase_User sends GET request to fetch scans for chatbot ID "<chatbot_id>"
    When FireBase_the user receives the scans response
    Then FireBase_the status code returned should be 200 for successful scans retrieval
    And FireBase_the response should contain an empty list of scans

    Examples:
      | chatbot_id                              |
      | 89ebd370-38bb-43e5-9956-5c8cda370b90     |

  @Test @Security
  Scenario Outline: FireBase_Verify scans API returns 400 for invalid chatbot ID format
    Given FireBase_User sends GET request to fetch scans for chatbot ID "<chatbot_id>"
    When FireBase_the user receives the scans response
    Then FireBase_the status code returned should be 400 for bad request error
    And FireBase_the response should contain an error message "Bad Request"
    And FireBase_the message should contain "Invalid input:"

    Examples:
      | chatbot_id   |
      | invalid      |
      | ' OR 1=1 --  |
      | <script>alert('XSS')</script> |


