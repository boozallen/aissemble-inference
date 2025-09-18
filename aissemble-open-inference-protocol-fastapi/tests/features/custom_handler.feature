Feature: Customization of aissemble OIP Handler
  User should be able to provide custom implementation of handler logic so that they can integrate user's logic with ML model.

  Scenario: Handler implementations have default server status methods
    Given custom implementation of dataplane handler that doesn't implement server methods
    When server status method is called
    Then affirmative is responded

  Scenario: Handler implementations have overridden server status methods.
    Given custom implementation of dataplane handler that override implement server methods
    When server status method is called
    Then custom logic is reponded
