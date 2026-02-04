Feature: Text Summarization with OIP Client
  As a developer using aiSSEMBLE Inference
  I want to summarize text documents using the sumy module
  So that I can extract key information from long articles

  Background:
    Given MLServer is running with the Sumy model

  Scenario: Summarize a short article
    Given I have a short article text
    When I run summarization using the OIP client
    Then I should receive a summary
    And the summary should be shorter than the original text
    And the summary should not be empty

  Scenario: Summarize a medium article
    Given I have a medium article text
    When I run summarization using the OIP client
    Then I should receive a summary
    And the summary should contain approximately 3 sentences

  Scenario: Summarize a long article
    Given I have a long article text
    When I run summarization using the OIP client with model "sumy-textrank"
    Then I should receive a summary
    And the summary should be significantly shorter than the original

  Scenario: Use different algorithm (LSA)
    Given I have a medium article text
    When I run summarization using the OIP client with model "sumy-lsa"
    Then I should receive a summary
    And the summary should contain approximately 5 sentences

  Scenario: Handle empty text gracefully
    Given I have empty text
    When I attempt to run summarization
    Then I should receive an error response

  Scenario: Verify summary quality
    Given I have a long article text
    When I run summarization using the OIP client
    Then I should receive a summary
    And the summary should contain key information from the article
    And the summary should be grammatically coherent
