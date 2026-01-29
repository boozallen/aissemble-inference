Feature: Sumy Module Integration
  As a developer using aiSSEMBLE OIP
  I want the sumy module to provide text summarization capabilities
  So that I can summarize text documents using various algorithms

  Background:
    Given the sumy module is installed

  Scenario: Runtime entry point is registered
    When I check the module registry
    Then the "sumy" runtime should be registered
    And the runtime class should be "SumyRuntime"

  Scenario: Translator entry point is registered
    When I check the module registry
    Then the "sumy" translator should be registered
    And the translator class should be "SumyTranslator"

  Scenario: Can retrieve SumyRuntime and SumyTranslator classes
    When I retrieve the "sumy" runtime from the registry
    Then the runtime class should be importable
    When I retrieve the "sumy" translator from the registry
    Then the translator class should be importable

  Scenario: Load model with TextRank algorithm
    Given a model settings file with algorithm "textrank"
    When I load the sumy runtime
    Then the runtime should be ready
    And the algorithm should be "textrank"

  Scenario: Load model with LSA algorithm
    Given a model settings file with algorithm "lsa"
    When I load the sumy runtime
    Then the runtime should be ready
    And the algorithm should be "lsa"

  Scenario: Summarize short text
    Given a model settings file with algorithm "textrank"
    And I load the sumy runtime
    And a short article text
    When I run inference on the text
    Then I should receive a summary
    And the summary should be shorter than the original text

  Scenario: Summarize long text
    Given a model settings file with algorithm "textrank"
    And I load the sumy runtime
    And a long article text with 10 paragraphs
    When I run inference on the text
    Then I should receive a summary
    And the summary should be shorter than the original text

  Scenario: Summary respects sentences_count parameter
    Given a model settings file with algorithm "textrank" and sentences_count 5
    And I load the sumy runtime
    And a long article text with 10 paragraphs
    When I run inference on the text
    Then I should receive a summary
    And the summary should contain approximately 5 sentences

  Scenario: TextRank algorithm produces valid summary
    Given a model settings file with algorithm "textrank"
    And I load the sumy runtime
    And a medium article text
    When I run inference on the text
    Then I should receive a summary
    And the summary should not be empty

  Scenario: LSA algorithm produces valid summary
    Given a model settings file with algorithm "lsa"
    And I load the sumy runtime
    And a medium article text
    When I run inference on the text
    Then I should receive a summary
    And the summary should not be empty

  Scenario: LexRank algorithm produces valid summary
    Given a model settings file with algorithm "lexrank"
    And I load the sumy runtime
    And a medium article text
    When I run inference on the text
    Then I should receive a summary
    And the summary should not be empty

  Scenario: Empty input text raises error
    Given a model settings file with algorithm "textrank"
    And I load the sumy runtime
    And an empty text input
    When I run inference on the text
    Then inference should raise a ValueError
    And the error message should mention "empty"

  Scenario: Invalid algorithm name raises error
    Given a model settings file with algorithm "invalid_algorithm"
    When I load the sumy runtime
    Then loading should raise a ValueError
    And the error message should mention "Unsupported algorithm"

  Scenario: Missing input tensor raises error
    Given a model settings file with algorithm "textrank"
    And I load the sumy runtime
    And an empty payload with no inputs
    When I run inference on the payload
    Then inference should raise a ValueError
    And the error message should mention "must contain at least one input"

  Scenario: Use sumy via InferenceClient
    Given a mock OIP adapter
    And the adapter returns a valid summary response
    When I use InferenceClient to summarize text
    Then I should receive a SummarizationResult
    And the result should contain the summary text

  @integration
  Scenario: Summarize text via OIP with MLServer and TextRank
    Given MLServer is running with Sumy model using "textrank" algorithm
    And I have an InferenceClient configured with HttpOipAdapter
    And I load a sample article from test data
    When I call summarize and provide the text
    Then I should receive a SummarizationResult via OIP
    And the summary should be shorter than the original text
    And the summary should not be empty

  @integration
  Scenario: Summarize text via OIP with MLServer and LSA
    Given MLServer is running with Sumy model using "lsa" algorithm
    And I have an InferenceClient configured with HttpOipAdapter
    And I load a sample article from test data
    When I call summarize and provide the text
    Then I should receive a SummarizationResult via OIP
    And the summary should be shorter than the original text

  @integration
  Scenario: Verify sentence count parameter via OIP
    Given MLServer is running with Sumy model using "textrank" algorithm with 5 sentences
    And I have an InferenceClient configured with HttpOipAdapter
    And I load a sample article from test data
    When I call summarize and provide the text
    Then I should receive a SummarizationResult via OIP
    And the summary should contain approximately 5 sentences via OIP
