Feature: Object Detection with OIP Client
  As a developer using the aiSSEMBLE Inference library
  I want to perform object detection on images
  So that I can identify and locate objects in my images

  Background:
    Given MLServer is running with the YOLOv8 model

  Scenario: Detect objects in an image using OIP client
    Given I have an image containing common objects
    When I run object detection using the OIP client
    Then I should receive detection results
    And the results should contain bounding boxes
    And the results should contain labels
    And the results should contain confidence scores

  Scenario: Filter detections by confidence threshold
    Given I have an image containing common objects
    When I run object detection with a confidence threshold of 0.5
    Then all returned detections should have confidence above 0.5
