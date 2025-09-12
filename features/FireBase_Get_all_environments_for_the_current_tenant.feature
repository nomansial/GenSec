Feature: FireBase_Get Environments

  @Test
  Scenario: FireBase_Valid API key returns environments
    Given FireBase_the user sends a GET request to retrieve the environments using APIKey
    When FireBase_the user receives the response
    Then FireBase_the status code returned should be 200
    And FireBase_each environment should have a non-null "env_id" and "name"

  @Test  @Security
  Scenario: FireBase_Invalid API Key denies access
    Given FireBase_the user sends a GET request to retrieve the environments using an invalid API key
    When FireBase_the user receives the response
    Then FireBase_status code be 401
    And FireBase_the response should contain code 401
    And FireBase_the response should contain the message Jwt is expired

  @Test  @Security
  Scenario: FireBase_SQL injection attempt in the API request
    Given FireBase_the user sends a GET request with a malicious payload
    When FireBase_the user receives the response
    Then FireBase_the response should contain the message Invalid input

  @Test  @Security
  Scenario: FireBase_XSS attack attempt in the API request
    Given FireBase_the user sends a GET request with a XSS attempt
    When FireBase_the user receives the response
    Then FireBase_the response should contain the message Invalid input
