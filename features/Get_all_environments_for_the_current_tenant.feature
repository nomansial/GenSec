Feature: Get Environments API

  @Test
  Scenario: Verify Get Environments API returns valid environments
    Given the user sends a GET request to retrieve the environments
    When the user receives the response
    Then the status code returned should be 200
    And each environment should have a non-null "env_id" and "name"
