Feature: FireBase_Create Environment API

  @Test @Negative @Security
  Scenario Outline: FireBase_Verify Create Environment API
    Given FireBase_the user provides the environment details "<env_name>" and "<env_description>"
    When FireBase_the user sends a request to create the environment
    Then FireBase_code should be <status_code>
    Then FireBase_the response should be validated based on error_message <error_message>

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
      | ' OR 1=1 --   | ' OR 1=1 --                                         | 400         | Bad Request   |
      | <script>alert('XSS')</script>| <script>alert('XSS')</script>        | 400         | Bad Request   |
