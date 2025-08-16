Feature: Update Environment API

  @Test
  Scenario Outline: Verify Update Environment API when environment is not found (Negative Case)
    Given User sends PUT request to update environment details with an invalid env_id "<env_id>"
    When user receives the response
    Then the status code should be 404 for not found error
    And the response should contain an error message "Not Found"
    And the message should be "Environment with ID "env_id" not found for update."

    Examples:
      | env_id                               |
      | ab809075-108f-4f67-2fb5-dc909ed60692 |
      | None                                 |
