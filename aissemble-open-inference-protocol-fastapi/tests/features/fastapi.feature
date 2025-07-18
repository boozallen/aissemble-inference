Feature: Test FastAPI OIP Implementation

  Scenario Outline: The default handler exposes OIP endpoints and the default authz adapter permits anonymous calls
    Given I have an OIP FastAPI app with the default handler
    When I send a "<method>" request to "<path>"
    Then the response status code should be <response_code>
    And the response should contain "<response>"

    Examples:
      |method | path                                 | response_code | response        |
      | GET   | /v2/models/my_model                  | 501           | Not Implemented |
      | GET   | /v2/models/my_model/versions/1       | 501           | Not Implemented |
      | GET   | /v2/models/my_model/ready            | 501           | Not Implemented |
      | GET   | /v2/models/my_model/versions/1/ready | 501           | Not Implemented |
      | GET   | /v2/health/ready                     | 200           | "live":true     |
      | GET   | /v2/health/live                      | 200           | "live":true     |
      | GET   | /v2                                  | 200           | "name":"FastAPI"|
      | POST  | /v2/models/my_model/infer            | 501           | Not Implemented |
      | POST  | /v2/models/my_model/versions/1/infer | 501           | Not Implemented |


  Scenario Outline: The OpenAPI schema exposes OIP endpoints
    Given I have an OIP FastAPI app with the default handler
    When I send a "<method>" request to "<path>"
    Then the response status code should be 200
    And the schema contains a "<expected_method>" path for "<expected_endpoint>"

    Examples:
      |method| path          | expected_method | expected_endpoint                                      |
      | GET  | /openapi.json | get             | /v2/models/{model_name}                                |
      | GET  | /openapi.json | get             | /v2/models/{model_name}/versions/{model_version}       |
      | GET  | /openapi.json | get             | /v2/models/{model_name}/ready                          |
      | GET  | /openapi.json | get             | /v2/models/{model_name}/versions/{model_version}/ready |
      | GET  | /openapi.json | get             | /v2/health/ready                                       |
      | GET  | /openapi.json | get             | /v2/health/live                                        |
      | GET  | /openapi.json | get             | /v2                                                    |
      | GET  | /openapi.json | post            | /v2/models/{model_name}/infer                          |
      | GET  | /openapi.json | post            | /v2/models/{model_name}/versions/{model_version}/infer |


  Scenario Outline: The default handler exposes OIP endpoints and the default authz adapter permits authenticated calls
    Given I have an OIP FastAPI app with the default handler
    When I send a "<method>" request to "<path>" with an authorization header
    Then the response status code should be <response_code>
    And the response should contain "<response>"

    Examples:
      |method | path                                 | response_code | response        |
      | GET   | /v2/models/my_model                  | 501           | Not Implemented |
      | GET   | /v2/models/my_model/versions/1       | 501           | Not Implemented |
      | GET   | /v2/models/my_model/ready            | 501           | Not Implemented |
      | GET   | /v2/models/my_model/versions/1/ready | 501           | Not Implemented |
      | GET   | /v2/health/ready                     | 200           | "live":true     |
      | GET   | /v2/health/live                      | 200           | "live":true     |
      | GET   | /v2                                  | 200           | "name":"FastAPI"|
      | POST  | /v2/models/my_model/infer            | 501           | Not Implemented |
      | POST  | /v2/models/my_model/versions/1/infer | 501           | Not Implemented |

  Scenario: The inference endpoint maps handlers response to the REST response object
    Given I have a handler that returns outputs data
    And I have an OIP FastAPI app with the handler
    And I have an infer request
    When I send a "POST" request to "/v2/models/my_model/infer"
    Then the response status code should be 200
    Then the response should contain "byte output data"
