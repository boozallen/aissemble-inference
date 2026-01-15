Feature: Invoke summarization functionality through InferenceClient

  Scenario: Invoke summarization through a mission-driven client
    Given an text on which we would like to perform summarization
    When the text is processed for summarization
    Then a summary is returned with a summary length