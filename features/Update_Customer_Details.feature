Feature: Update Customer Details API

  @Test
  Scenario Outline: Verify Update Customer API updates user details successfully with different data
    Given User sends PUT request to update customer details with "<first_name>", "<last_name>", "<job_title>", "<new_password>", and "<phone_number>"
    When the user receives the response from update customer API
    Then the response should contain a message "User updated successfully"

    Examples:
      | first_name  | last_name | job_title            | new_password | phone_number   |
      | Automation  | Update    | Test Automation Lead | Test@123     | +971508078631  |




  @Test @Negative @Security
  Scenario Outline: Verify Update Customer API returns error when invalid or empty parameters are passed
    Given User sends PUT request to update customer details with "<first_name>", "<last_name>", "<job_title>", "<new_password>", and "<phone_number>"
    When the user receives the response from update customer API
    Then the response should contain an error message "Invalid input"
    And the response should contain "Invalid input:" in response body

    Examples:
      | first_name | last_name | job_title | new_password | phone_number |
      |   None         | None           | None           | None              | None              |
      |' OR '1'='1     |' OR '1'='1     |' OR '1'='1     |' OR '1'='1        |' OR '1'='1        |


