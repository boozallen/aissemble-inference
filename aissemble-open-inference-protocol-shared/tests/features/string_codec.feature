Feature: StringCodec encoding and decoding

  Scenario: Decode InferenceRequest with request level content_type
    Given an InferenceRequest with string content_type at the request level and payload ["hello", "world"]
    When the payload is decoded
    Then the result should be a list of strings matching ["hello", "world"]

  Scenario: Decode InferenceRequest with input level content_type
    Given an InferenceRequest with string content_type at the input level and payload ["foo", "bar"]
    When the payload is decoded
    Then the result should be a list of strings matching ["foo", "bar"]

  Scenario: Encode payload into InferenceResponse
    Given a payload with type string ["wombat", "llama"]
    When the payload is encoded at the response level
    Then the result should be an InferenceResponse

  Scenario: Encode payload into ResponseOutput
    Given a payload with type string ["spam", "eggs"]
    When the payload is encoded at the request level
    Then the result should be a ResponseOutput