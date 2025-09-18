Feature: Test KServe Custom Handler Implementation

  Scenario Outline: KServeDataplaneHandler calls CustomDataplaneHandler to process OIP endpoints logics correctly.
    Given KServeDataplaneHandler and CustomDataplaneHandler
    When <method> is executed using the KServeDataplaneHandler
    Then CustomDataplaneHandler gets called to handle <method>
    And <method> is successful


    Examples:
      | method            |
      | model_ready       |
      | model_metadata    |
      | infer             |
      | server_ready      |
      | server_live       |
      | server_metadata   |
