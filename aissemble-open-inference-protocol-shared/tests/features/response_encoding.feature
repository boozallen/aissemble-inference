  Feature: Response encoding
  
  Scenario: Handler content type takes precedence over request content type
    Given a handler returns output "result" with content type "str"
    And a request asks for output "result" with content type "fp32"
    When the response is processed
    Then output "result" should use content type "str"

  Scenario: Request content type is used when handler has no content type
    Given a handler returns output "result" without content type
    And a request asks for output "result" with content type "str"
    When the response is processed
    Then output "result" should use content type "str"

  Scenario: Request-level content type applies to all outputs
    Given a handler returns output "result" without content type
    And a request asks for content type "str" at request level
    When the response is processed
    Then all outputs should use content type "str"