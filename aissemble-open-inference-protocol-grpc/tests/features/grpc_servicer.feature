
Feature: Tests aissemble-open-inference-protocol-gRPC servicer functionality

  Scenario: When an inference request is sent to the gRPC servicer, it is successfully routed to the handler
    Given a handler to perform inferencing exists
    And an aissemble oip gRPC servicer exists with the handler
    And an infer request exists
    When an infer request is sent to the gRPC servicer
    Then the handler receives the request with the expected data

  Scenario: When the custom handler returns an inference response, the gRPC servicer successfully returns the data
    Given a handler to perform inferencing exists
    And an aissemble oip gRPC servicer exists with the handler
    And the handler has model inferencing results
    When an infer response is sent to the handler
    Then the servicer's response corresponds to the handler's results