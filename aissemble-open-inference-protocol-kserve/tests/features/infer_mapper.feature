Feature: Test KServe Mapper Implementation

  Scenario: Map KServe InferRequest to aiSSEMBLE OIP InferenceRequest
    Given an InferRequest with KServe
    When InferRequest for KServe is converted to InferenceRequest for the dataplane handler
    Then InferenceRequest is correctly returned

  Scenario: Map KServe InferRequest to aiSSEMBLE OIP InferenceRequest
    Given an InferRequest with KServe
    When InferRequest for KServe is converted to InferenceRequest for the dataplane handler
    Then InferenceRequest is correctly returned


  Scenario: Map aiSSEMBLE OIP InferenceResponse to KServe InferResponse, Output TensorData is 2D
    Given an InferenceResponse with the dataplane handler with 2D TensorData
    When InferenceResponse for the dataplane handler is converted to InferResponse for KServe
    Then InferResponse is correctly returned


  Scenario: Map aiSSEMBLE OIP InferenceResponse to KServe InferResponse Output TensorData is 1D
    Given an InferenceResponse with the dataplane handler with 1D TensorData
    When InferenceResponse for the dataplane handler is converted to InferResponse for KServe
    Then InferResponse is correctly returned
