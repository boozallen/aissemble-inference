Feature: OIP Configuration Management

  Scenario: Configurations use defaults when no overrides provided
    Given no config overrides are provided
    When I create an OIPConfig instance
    Then the following configuration values should be returned
      | config                   | expected_value |
      | kserve_http_port         | 8080           |
      | kserve_enable_grpc       | True           |
      | kserve_access_log_format | None           |
      | fastapi_host             | 127.0.0.1      |
      | fastapi_port             | 8082           |
      | grpc_workers             | 3              |
      | auth_enabled             | True           |

  Scenario: Configurations use Krausening values when provided
    Given the configs are set via krausening properties
    When I create an OIPConfig instance
    Then the following configuration values should be returned
      | config                       | expected_value |
      | kserve_http_port             | 9090           |
      | kserve_enable_grpc           | False          |
      | kserve_access_log_format     | custom-format  |
      | fastapi_host                 | 192.168.1.1    |
      | fastapi_port                 | 9091           |
      | grpc_workers                 | 5              |
      | auth_enabled                 | False          |

  Scenario: Configurations use environment variables when provided
    Given the configs are set via environment variables
    When I create an OIPConfig instance
    Then the following configuration values should be returned
      | config           | expected_value       |
      | kserve_grpc_port | 7070                 |
      | kserve_workers   | 2                    |
      | fastapi_port     | 9082                 |
      | grpc_host        | 10.0.0.1             |
      | auth_algorithm   | RS256                |
      | pdp_url          | http://test:8080/pdp |


  Scenario: Configurations use KServe arguments when provided
    Given the configs are set via kserve arguments
    When I create an OIPConfig instance
    Then the following configuration values should be returned
      | config                        | expected_value |
      | kserve_http_port              | 9080           |
      | kserve_grpc_port              | 9081           |
      | kserve_workers                | 3              |
      | kserve_max_threads            | 8              |
      | kserve_max_asyncio_workers    | 2              |
      | kserve_enable_grpc            | False          |
      | kserve_enable_docs_url        | True           |
      | kserve_enable_latency_logging | False          |
      | kserve_access_log_format      | arg-log-format |

  Scenario Outline: Configuration precedence follows args > env > krausening > defaults
    Given kserve_http_port has krausening <krausening_value>, env <env_value>, and args <arg_value>
    When I create an OIPConfig instance
    Then the configuration kserve_http_port should have value <expected_value>
    Examples: Configuration precedence testing
      | krausening_value | env_value | arg_value | expected_value |
      | 9090             | None      | None      | 9090           |
      | 9090             | 7080      | None      | 7080           |
      | 9090             | 7080      | 6080      | 6080           |
      | 9090             | None      | 6080      | 6080           |