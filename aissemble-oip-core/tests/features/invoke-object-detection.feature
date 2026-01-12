Feature: Invoke object detection functionality through InferenceClient

  Scenario: Invoke object detection through mission-driven client
    Given an image on which we would like to perform object detection
    When the image is processed for object detection
    Then a result is returned with detected objects and their associated labels, scores, and bounding box coordinates