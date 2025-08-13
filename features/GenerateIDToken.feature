Feature: Manual Merchant Registration

  @Test
  Scenario Outline: Verify Firebase Token API
    Given the user provides the email "<email>", password "<password>", returnSecureToken "<returnSecureToken>", and tenantId "<tenantId>"
    When the user executes the API with the provided credentials
    Then the status code should be <statusCode>
    And the error message should be "<errorMessage>"
    Examples:
      # Positive Test Case
      | email                   | password                | returnSecureToken | tenantId                | statusCode | errorMessage                             |
      | noman.sial9@gmail.com    | *uWR=t7of#hUspATR+4I  | true              | SampleTenantB-1yak0   | 200        | ""                                     |

