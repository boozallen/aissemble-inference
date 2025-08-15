Feature: Validate that request/responses are OIP-compliant


  Scenario Outline: ResponseOutput/RequestInput shape validation
    Given a <request_response> whose shape is <expected_shape>
    And a data field whose value is <actual_data>
    When the <request_response> shape is validated
    Then the validation is <result>
    Examples:
      | request_response | expected_shape | actual_data         | result         |
      | RequestInput     | [2,2]          | [[1.0, 2.0],[3.0]]  | "unsuccessful" |
      | RequestInput     | [1,2]          | [[b"a"],[b"b"]]     | "unsuccessful" |
      | ResponseOutput   | [3]            | [True, False, True] | "successful"   |
      | ResponseOutput   | [2,2]          | [[1,2],[3,4]]       | "successful"   |


  Scenario Outline: ResponseOutput/RequestInput datatype validation
    Given a <request_response> whose datatype is <expected_datatype>
    And a data field whose value is <actual_data>
    When the <request_response> datatype is validated
    Then the validation is <result>
    Examples:
      | request_response | expected_datatype | actual_data                | result          |
      | RequestInput     | FP64              | [[0.1],[1.2],[4.0]]        | "successful"    |
      | RequestInput     | FP64              | [[0.1],["foo"]]            | "unsuccessful"  |
      | RequestInput     | BOOL              | [True,"False"]             | "unsuccessful"  |
      | ResponseOutput   | INT64             | 77                         | "successful"    |
      | ResponseOutput   | UINT32            | [0,1,2]                    | "successful"    |
      | ResponseOutput   | BYTES             | [[b"a",b"b"],[b"c",b"d"]]  | "successful"    |


  Scenario Outline: InferenceResponse/InferenceRequest shape and datatype validation
    Given an <inference_request_response> with name <name>, shape <expected_shape>, datatype <expected_datatype>, and data <actual_data>
    When the <inference_request_response> is validated
    Then the validation is <result>
    Examples:
      | inference_request_response | name     | expected_shape  | expected_datatype  | actual_data      | result          |
      | InferenceRequest           | input-0  | [1,1]           | INT64              | [[11]]           | "successful"    |
      | InferenceRequest           | input-1  | []              | FP64               | None             | "unsuccessful"  |
      | InferenceResponse          | output-0 | [2,1]           | BYTES              | [[0.1],["foo"]]  | "unsuccessful"  |
      | InferenceResponse          | output-1 | [3,4]           | BOOL               | None             | "unsuccessful"  |


  Scenario Outline: Input shape is valid if the desired shape is dynamic
    Given an input shape of <actual_data> is given and <desired_shape> is desired
    When the input shape validation is performed
    Then the shape validation is <valid>
    Examples:
      | actual_data               | desired_shape | valid |
      | [[1,2],[1,2],[4,0]]       | [3,2]         | True  |
      | [[1,2,3],[1,2],[4,0,5,6]] | [3,-1]        | True  |
      | [[1,3],[1,3],[1,3]]       | [-1,2]        | True  |
      | [2,99]                    | [2,-1]        | False |
      | [[6],[3,1,2],[]]          | [3,-1]        | True  |
