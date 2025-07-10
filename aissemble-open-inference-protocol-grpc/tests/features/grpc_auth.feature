Feature: gRPC Authentication

  Scenario: Call a protected endpoint with a valid JWT
    Given an AuthInterceptor protecting the endpoint
    And a valid JWT token
    When a request is made to the protected endpoint
    Then the response is successful

  Scenario: Call a protected endpoint with an invalid JWT
    Given an AuthInterceptor protecting the endpoint
    And an invalid JWT token
    When a request is made to the protected endpoint
    Then the response is UNAUTHENTICATED

  Scenario: Call a protected endpoint with no JWT
    Given an AuthInterceptor protecting the endpoint
    When a request is made to the protected endpoint
    Then the response is UNAUTHENTICATED