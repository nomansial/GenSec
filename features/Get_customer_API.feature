Feature: Verify Get Customer API Key

  @Test
  Scenario: Verify Get Customer API Key retrieves customer API key successfully
    Given User sends GET request to fetch customer API key
    When the user receives the response
    Then the status code returned should be 200 for a successful request for get customer API
    And the response should contain the customer API key details
    And all the parameters in the response should not be None

  @Test @Negative @Security
  Scenario: Verify Get Customer API Key returns error when API key is missing or invalid
    Given User sends GET request to fetch customer API key with invalid or missing API key
    When the user receives the response
    Then the status code returned should be 401 for unauthorized request
    And the response should contain an error message for customer API
    And the error message should state "Invalid or missing API key"
