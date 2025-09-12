Feature: FireBase_Delete Environment API

  @Test
  Scenario: FireBase_Verify Delete Environment API deletes the environment
    Given FireBase_User fetches env_id from Create Environment API
    When FireBase_user sends delete API call
    Then FireBase_the status code returned should be 200 for the delete environment
    And FireBase_contain a "status" of "Deleted"
    And FireBase_contain the correct "env_id"
    And FireBase_should have a non-null "name"

  @Test @Negative
  Scenario: FireBase_Verify Delete Environment API returns 404 for non-existent env_id
    Given FireBase_User sets an invalid env_id
    When FireBase_delete API call is triggered
    Then FireBase_contain an error message "Environment not found"


  @Test @Security
  Scenario: FireBase_Verify Delete Environment API handles injection attack safely
    Given FireBase_User sets a malicious env_id for injection attack
    When FireBase_user sends delete API call for security scenrio
    Then FireBase_error contains "Bad Request"


