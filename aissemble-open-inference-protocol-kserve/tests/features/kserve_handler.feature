Feature: Test KServe Custom Handler Implementation

  Scenario: Handler implementation loads model correctly.
    Given KServe custom handler with ability to load keras model
    When Load API executed using the KServe custom handler
    Then load is successful and model server status is set to ready