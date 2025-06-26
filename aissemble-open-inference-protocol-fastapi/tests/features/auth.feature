Feature: Authentication and authorization

  Scenario: A XACML 3.0 request can be generated
    Given I have a user with a role
    When I build a XACML 3.0 request
    Then the request is properly constructed
