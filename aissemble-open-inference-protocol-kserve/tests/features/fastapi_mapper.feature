Feature: Test KServe Converter Implementation

  Scenario: Map Kserve InferRequest to FastAPI InferenceRequest
    Given an InferRequest with KServe
    When InferRequest for KServe is converted to InferenceRequest for the dataplane handler
    Then InferenceRequest is correctly returned

  Scenario: Map FastAPI InferenceResponse to KServe InferResponse
    Given an InferenceResponse with the dataplane handler
    When InferenceResponse for the dataplane handler is converted to InferResponse for KServe
    Then InferResponse is correctly returned
