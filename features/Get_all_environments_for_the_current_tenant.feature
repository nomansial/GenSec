Feature: Get Environments

  @Test
  Scenario: Valid API key returns environments
    Given the user sends a GET request to retrieve the environments using APIKey
    When the user receives the response
    Then the status code returned should be 200
    And each environment should have a non-null "env_id" and "name"

  @Test @Negative
  Scenario: APIKey2 should not have access to environments visible to APIKey
    Given the user sends a GET request to retrieve the environments using APIKey
    Then the user stores the list of environments returned
    Given the user sends a GET request to retrieve the environments using APIKey2
    When the user receives the response
    Then the status code returned should be 200
    And the environments returned should not match those from APIKey

  @Test @Security
  Scenario: Invalid API Key denies access
    Given the user sends a GET request to retrieve the environments using an invalid API key
    When the user receives the response
    Then status code be 400
    And the response should contain code 400
    And the response should contain the message "INVALID_ARGUMENT:"

  @Test @Security
  Scenario: SQL injection attempt in the API request
    Given the user sends a GET request with a malicious payload
    When the user receives the response
    Then the response should contain the message Invalid input

  @Test @Security
  Scenario: XSS attack attempt in the API request
    Given the user sends a GET request with a XSS attempt
    When the user receives the response
    Then the response should contain the message Invalid input
