Feature: Retrieve Environments

  @Test
  Scenario: Valid API key returns environments
    Given the user sends a GET request to retrieve the environments using APIKey
    When the user receives the response
    Then the status code returned should be 200
    And each environment should have a non-null "env_id" and "name"

  @Test
  Scenario: APIKey2 should not have access to environments visible to APIKey
    Given the user sends a GET request to retrieve the environments using APIKey
    Then the user stores the list of environments returned
    Given the user sends a GET request to retrieve the environments using APIKey2
    When the user receives the response
    Then the status code returned should be 200
    And the environments returned should not match those from APIKey