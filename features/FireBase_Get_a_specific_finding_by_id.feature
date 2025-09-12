Feature: FireBase_Get Finding Details by Finding ID using Genr3d API


  @Test
  Scenario Outline: FireBase_Validate finding details response for a valid finding ID
    Given FireBase_User sends GET request to fetch finding details for finding ID "<finding_id>"
    When FireBase_the user receives the finding details response
    Then FireBase_the status code returned should be 200 for successful finding retrieval
    And FireBase_the response should contain a valid "finding_id" matching "<finding_id>"
    And FireBase_the response should contain a valid "scan_id" of length 36
    And FireBase_the response should contain a valid "chatbot_id" of length 36
    And FireBase_contain a non-empty "chatbot_name"
    And FireBase_contain a non-empty "finding_name"
    And FireBase_contain a non-empty "description"
    And FireBase_contain a non-empty "evidence"
    And FireBase_contain a non-empty "mitigation"
    And FireBase_contain a non-empty "risk"
    And FireBase_contain a non-empty "severity"
    And FireBase_the response should contain a "creation_timestamp" in ISO 8601 format
    And FireBase_the response should contain non-empty lists for "data_classification" and "data_targeted"

    Examples:
      | finding_id                             |
      | 213a1750-e18e-4dc3-bfc8-b54b834852d0    |

  @Test @Negative
  Scenario Outline: FireBase_Validate finding details response when finding ID is not found
    Given FireBase_User sends GET request to fetch finding details for finding ID "<finding_id>"
    When FireBase_the user receives the finding details response
    Then FireBase_the status code returned should be 404 for not found error
    And FireBase_the response should contain an error message "Not Found"
    And FireBase_the message should contain "Finding with ID <finding_id> not found."

    Examples:
      | finding_id                             |
      | 213a1750-e18e-4dc3-bfc8-b54b83485200   |

  @Test @Negative @Security
  Scenario Outline: FireBase_Validate finding details response for invalid finding ID format
    Given FireBase_User sends GET request to fetch finding details for finding ID "<finding_id>"
    When FireBase_the user receives the finding details response
    Then FireBase_the status code returned should be 400 for bad request error
    And FireBase_the response should contain an error message "Bad Request"
    And FireBase_the message should contain "Invalid input:"

    Examples:
      | finding_id   |
      | invalid      |
      | ' OR 1=1 --  |

  @Test @Security
  Scenario: FireBase_XSS injection attempt in finding ID "<script>alert('XSS');</script>"
    Given FireBase_the user sends GET request with finding ID
    When FireBase_the user receives the response
    Then FireBase_the status code returned should be 404
    And FireBase_the message should contain "The current request is not defined by this API."


