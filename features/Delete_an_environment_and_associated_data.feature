Feature: Delete Environment API

  @Test
  Scenario: Verify Delete Environment API deletes the environment
    Given User fetches env_id from Create Environment API
    When user sends delete API call
    Then the status code returned should be 200 for the delete environment
    And contain a "status" of "Deleted"
    And contain the correct "env_id"
    And should have a non-null "name"

  @Test @Negative
  Scenario: Verify Delete Environment API returns 404 for non-existent env_id
    Given User sets an invalid env_id
    When delete API call is triggered
    Then contain an error message "Environment not found"


  @Test @Security
  Scenario: Verify Delete Environment API handles injection attack safely
    Given User sets a malicious env_id for injection attack
    When user sends delete API call for security scenrio
    Then error contains "Bad Request"


