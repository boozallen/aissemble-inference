Feature: Customization of aissemble OIP Model Handler
  User should be able to provide custom implementation of the model handler logic so that they can integrate user's
  logic with ML model.

  Scenario: Model Handler implementations have default model ready method
    Given custom implementation of model handler that doesn't implement the model ready method
    When model ready method is called
    Then affirmative is responded
    And default logic is responded

  Scenario: Handler implementations have overridden server status methods.
    Given custom implementation of model handler that overrides implement the model ready method
    When model ready method is called
    Then affirmative is responded
    And custom logic is responded
