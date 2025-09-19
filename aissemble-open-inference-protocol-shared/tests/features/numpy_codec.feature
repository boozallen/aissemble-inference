Feature: NumpyCodec encoding and decoding

  Scenario: Decode InferenceRequest with request level content_type
    Given an InferenceRequest with numpy content_type at the request level and payload [1, 2, 3, 4]
    When the payload is decoded
    Then the result should be a numpy array matching [1, 2, 3, 4]

  Scenario: Decode InferenceRequest with input level content_type
    Given an InferenceRequest with numpy content_type at the input level and payload [5, 6, 7, 8]
    When the numpy payload is decoded
    Then the result should be a numpy array matching [5, 6, 7, 8]

  Scenario: Decode InferenceRequest with input level content_type and multiple inputs
    Given an InferenceRequest with numpy content_type at the input level and multiple numpy inputs
    When the numpy payload is decoded
    Then the result should be a multiple outputs with type numpy array

  Scenario: Decode InferenceRequest with numpy multi-dimensional payload
    Given an InferenceRequest with numpy content_type at the request level and multi-dimensional payload [[17, 18], [19, 20], [21, 22]]
    When the numpy payload is decoded
    Then the result should be a numpy array matching [[17, 18], [19, 20], [21, 22]]

  Scenario: Encode payload into InferenceResponse
    Given a payload with type numpy [9, 10, 11, 12]
    When I encode the payload at the response level
    Then the result should be a numpy InferenceResponse

  Scenario: Encode payload into ResponseOutput
    Given a payload with type numpy [13, 14, 15 ,16]
    When I encode the payload at the request level
    Then the result should be a numpy ResponseOutput