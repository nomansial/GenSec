Feature: FireBase_Update Environment API

  @Test
  Scenario: FireBase_Verify Update Environment API updates the environment successfully
    Given FireBase_User fetches env_id from Create Environment API
    When FireBase_user sends the update API call with new environment details
    Then FireBase_the status code returned should be 200 for the updated environment
    And FireBase_the response should contain a "status" of "Updated"
    And FireBase_the response should contain the env_id in the updated response

  @Test @Negative
  Scenario Outline: FireBase_Verify Update Environment API when environment is not found (Negative Case)
    Given FireBase_User sends PUT request to update environment details with an invalid env_id "<env_id>"
    When FireBase_user receives the response
    Then FireBase_the status code should be 404 for not found error
    And FireBase_the response should contain an error message "Not Found"
    And FireBase_the message should be "Environment with ID "env_id" not found for update."

    Examples:
      | env_id                               |
      | ab809075-108f-4f67-2fb5-dc909ed60692 |
      | None                                 |

  @Test @Security
  Scenario Outline: FireBase_SQL injection attempt in the Update Environment API request
    Given FireBase_User sends POST request to update environment details with "<env_id>" and "<env_name>" and "<env_description>"
    When FireBase_user receives the response
    Then FireBase_the response should contain the error message "Bad Request" for SQL injection input
    And FireBase_the response message should contain "Invalid input:"

    Examples:
      | env_id      | env_name    | env_description |
      | ' OR 1=1 -- | ' OR 1=1 -- | ' OR 1=1 --     |
