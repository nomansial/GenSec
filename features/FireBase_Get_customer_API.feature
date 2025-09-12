Feature: FireBase_Verify Get Customer API Key

  @Test
  Scenario: FireBase_Verify Get Customer API Key retrieves customer API key successfully
    Given FireBase_User sends GET request to fetch customer API key
    When FireBase_the user receives the response
    Then FireBase_the status code returned should be 200 for a successful request for get customer API
    And FireBase_the response should contain the customer API key details
    And FireBase_all the parameters in the response should not be None

  @Test @Negative @Security
  Scenario: FireBase_Verify Get Customer API Key returns error when API key is missing or invalid
    Given FireBase_User sends GET request to fetch customer API key with invalid or missing API key
    When FireBase_the user receives the response
    Then FireBase_the status code returned should be 401 for unauthorized request
    And FireBase_the response should contain an error message for customer API
    And FireBase_the error message should state "Invalid or missing API key"
