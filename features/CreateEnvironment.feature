Feature: Create Environment API

  @Test
  Scenario Outline: Verify Create Environment API
    Given the user provides the environment details "<env_name>" and "<env_description>"
    When the user sends a request to create the environment
    Then code should be <status_code>
    Then the response should be validated based on error_message <error_message>

    Examples:
      # Positive and Negative Test Cases
      | env_name      | env_description                                     | status_code | error_message |
      | Automation QA | System testing please ignore                        | 200         | None          |
      | None          | None                                                | 400         | Bad Request   |
      | AB            | Te                                                  | 400         | Bad Request   |
      | X             | A                                                   | 400         | Bad Request   |
      | Invalid@Name  | Invalid@Desc                                        | 400         | Bad Request   |
      | None          | Valid description                                   | 400         | Bad Request   |
      | Valid Name    | None                                                | 400         | Bad Request   |
