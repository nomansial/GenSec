Feature: Delete Environment API

  @Test
  Scenario: Verify Delete Environment API deletes the environment
    Given User fetches env_id from Create Environment API
    When user sends delete API call
    Then the status code returned should be 200 for the delete environment
    And contain a "status" of "Deleted"
    And contain the correct "env_id"
    And should have a non-null "name"
