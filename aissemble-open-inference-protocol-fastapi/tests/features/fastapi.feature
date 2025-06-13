Feature: Test FastAPI OIP Implementation

  Scenario Outline: The default handler exposes OIP endpoints
    Given I have an OIP FastAPI app with the default handler
    When I send a "<method>" request to "<path>"
    Then the response status code should be 501
    And the response should contain "Not Implemented"

    Examples:
      |method | path                                 |
      | GET   | /v2/models/my_model                  |
      | GET   | /v2/models/my_model/versions/1       |
      | GET   | /v2/models/my_model/ready            |
      | GET   | /v2/models/my_model/versions/1/ready |
      | GET   | /v2/health/ready                     |
      | GET   | /v2/health/live                      |
      | GET   | /v2                                  |
      | POST  | /v2/models/my_model/infer            |
      | POST  | /v2/models/my_model/versions/1/infer |


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
