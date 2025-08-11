Feature: Tests aissemble-open-inference-protocol-gRPC servicer functionality

  Scenario: When an inference request is sent to the gRPC servicer, it is successfully routed to the handler
    Given a handler to perform the request exists
    And an aissemble oip gRPC servicer exists with the handler
    And an infer request exists
    When an infer request is sent to the gRPC servicer
    Then the handler receives the request with the expected data

  Scenario: When the custom handler returns an inference response, the gRPC servicer successfully returns the data
    Given a handler to perform the request exists
    And an aissemble oip gRPC servicer exists with the handler
    And the handler has model inferencing results
    When an infer response is sent to the handler
    Then the servicer's response corresponds to the handler's results

  Scenario: When a Model metadata request is sent to the gRPC servicer, it routes to the handler and returns the handler's model metadata
    Given a handler to perform the request exists
    And an aissemble oip gRPC servicer exists with the handler
    And a model metadata request exists
    When the model metadata request is sent to the gRPC servicer
    Then the handler receives the model metadata request with the expected data
    And the servicer's model metadata response corresponds to the handler's results

  Scenario: When a model ready requests is sent to the gRPC servicer, it routes to the handler and returns then
  handlers model metadata
    Given a handler to perform the request exists
    And an aissemble oip gRPC servicer exists with the handler
    And a model ready request exists
    When the model ready request is sent to the gRPC servicer
    Then the handler receives the model ready request with the expected data
    And the servicer's model ready response corresponds to the handler's results

  Scenario: When a server metadata requests is sent to the gRPC servicer, it routes to the handler and returns then
  handlers model metadata
    Given a handler to perform the request exists
    And an aissemble oip gRPC servicer exists with the handler
    And a server metadata request exists
    When the server metadata request is sent to the gRPC servicer
    Then the servicer's server metadata response corresponds to the handler's results

  Scenario: When a server ready requests is sent to the gRPC servicer, it routes to the handler and returns then
  handlers model metadata
    Given a handler to perform the request exists
    And an aissemble oip gRPC servicer exists with the handler
    And a server ready request exists
    When the server ready request is sent to the gRPC servicer
    Then the servicer's server ready response corresponds to the handler's results

  Scenario: When a server live requests is sent to the gRPC servicer, it routes to the handler and returns then
  handlers model metadata
    Given a handler to perform the request exists
    And an aissemble oip gRPC servicer exists with the handler
    And a server live request exists
    When the server live request is sent to the gRPC servicer
    Then the servicer's server live response corresponds to the handler's results
