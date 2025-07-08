
Feature: Tests aissemble-open-inference-protocol-gRPC servicer functionality

  Scenario: When an inference request is sent to the gRPC servicer, it is successfully routed to the handler
    Given a handler to perform inferencing exists
    And an aissemble oip gRPC servicer exists with the handler
    And an infer request exists
    When an infer request is sent to the gRPC servicer
    Then the handler receives the request with the expected data
