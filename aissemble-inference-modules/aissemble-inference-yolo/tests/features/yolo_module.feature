Feature: YOLO Module Capabilities
  As a developer using the aiSSEMBLE Inference library
  I want to use the YOLO module for object detection
  So that I can detect objects in images using various YOLO model versions

  # ============================================
  # Module Discovery and Registration
  # ============================================

  Scenario: YOLO module registers via entry points
    Given the aissemble-inference-yolo package is installed
    When I query the ModuleRegistry for available modules
    Then the "yolo" runtime should be listed
    And the "yolo" translator should be listed

  Scenario: YOLO runtime class is retrievable from registry
    Given the aissemble-inference-yolo package is installed
    When I retrieve the "yolo" runtime from the registry
    Then I should receive the YOLORuntime class

  Scenario: YOLO translator class is retrievable from registry
    Given the aissemble-inference-yolo package is installed
    When I retrieve the "yolo" translator from the registry
    Then I should receive the YOLOTranslator class

  # ============================================
  # Model Loading - Known Models
  # ============================================

  Scenario Outline: Load models
    Given MLServer is configured with model variant "<modelVariant>"
    When the YOLORuntime loads the model
    Then the model should load successfully
    And the runtime should be ready for inference

    Examples:
      | modelVariant | modelDescription                     |
      | yolov8n.pt   | YOLOv8 nano model                    |
      | yolov8s.pt   | YOLOv8 small model                   |
      | yolov5nu.pt  | YOLOv5 nano model (with ultralytics) |

  Scenario: Load default model when no variant specified
    Given MLServer is configured without a model variant parameter
    When the YOLORuntime loads the model
    Then the model should load successfully
    And the default "yolov8n.pt" model should be used

  # ============================================
  # Model Loading - Unknown/Invalid Models
  # ============================================

  Scenario: Attempt to load non-existent model variant
    Given MLServer is configured with model variant "yolov99-nonexistent.pt"
    When the YOLORuntime attempts to load the model
    Then the model loading should fail with an appropriate error

  Scenario: Attempt to load model with invalid path
    Given MLServer is configured with model variant "/invalid/path/model.pt"
    When the YOLORuntime attempts to load the model
    Then the model loading should fail with an appropriate error

  # ============================================
  # Inference - Image Processing
  # ============================================

  Scenario Outline: Process base64-encoded images
    Given a YOLOv8 model is loaded and ready
    And I have a base64-encoded "<imageType>" image
    When I send the image for inference
    Then I should receive a valid inference response

    Examples:
      | imageType |
      | PNG       |
      | JPEG      |

  Scenario: Process image with detectable objects
    Given a YOLOv8 model is loaded and ready
    And I have an image containing a person
    When I send the image for inference
    Then I should receive detections in the response
    And at least one detection should have label "person"

  Scenario: Process image with no detectable objects
    Given a YOLOv8 model is loaded and ready
    And I have a blank white image
    When I send the image for inference
    Then I should receive an empty detections list
    And the response should still be valid OIP format

  Scenario: Process image with multiple objects
    Given a YOLOv8 model is loaded and ready
    And I have an image containing multiple objects
    When I send the image for inference
    Then I should receive multiple detections
    And each detection should have a unique bounding box

  # ============================================
  # Inference - Response Format Validation
  # ============================================

  Scenario: Response contains required output tensors
    Given a YOLOv8 model is loaded and ready
    And I have an image for inference
    When I send the image for inference
    Then the response should contain a "bboxes" output
    And the response should contain a "labels" output
    And the response should contain a "scores" output

  Scenario: Bounding box format is correct
    Given a YOLOv8 model is loaded and ready
    And I have an image with detectable objects
    When I send the image for inference
    Then each bounding box should have 4 coordinates
    And coordinates should be in x1, y1, x2, y2 format
    And x2 should be greater than x1
    And y2 should be greater than y1

  Scenario: Confidence scores are in valid range
    Given a YOLOv8 model is loaded and ready
    And I have an image with detectable objects
    When I send the image for inference
    Then all confidence scores should be between 0 and 1

  Scenario: Labels are valid COCO class names
    Given a YOLOv8 model is loaded and ready
    And I have an image with detectable objects
    When I send the image for inference
    Then all labels should be non-empty strings
    And labels should be from the COCO dataset classes

  Scenario: Output tensor shapes are consistent
    Given a YOLOv8 model is loaded and ready
    And I have an image with detectable objects
    When I send the image for inference
    Then the number of bounding boxes should equal the number of labels
    And the number of labels should equal the number of scores

  # ============================================
  # Inference - Error Handling
  # ============================================

  Scenario: Handle malformed base64 input
    Given a YOLOv8 model is loaded and ready
    When I send invalid base64 data for inference
    Then I should receive an error response

  Scenario: Handle empty input
    Given a YOLOv8 model is loaded and ready
    When I send an empty input for inference
    Then I should receive an error response

  Scenario: Handle non-image base64 data
    Given a YOLOv8 model is loaded and ready
    When I send base64-encoded text data for inference
    Then I should receive an error response

  # ============================================
  # Translator Functionality
  # ============================================

  Scenario: YOLOTranslator preprocesses PIL image
    Given I have a PIL Image object
    When I preprocess it with YOLOTranslator
    Then I should receive a valid OipRequest
    And the request should contain base64-encoded image data

  Scenario: YOLOTranslator preprocesses file path
    Given I have a path to an image file
    When I preprocess it with YOLOTranslator
    Then I should receive a valid OipRequest

  Scenario: YOLOTranslator preprocesses numpy array
    Given I have a numpy array representing an image
    When I preprocess it with YOLOTranslator
    Then I should receive a valid OipRequest

  Scenario: YOLOTranslator postprocesses valid response
    Given I have a valid OipResponse with detections
    When I postprocess it with YOLOTranslator
    Then I should receive an ObjectDetectionResult from the translator
    And the result should contain Detection objects

  Scenario: YOLOTranslator handles response with no detections
    Given I have a valid OipResponse with zero detections
    When I postprocess it with YOLOTranslator
    Then I should receive an ObjectDetectionResult from the translator
    And the result should have an empty detections list

  # ============================================
  # Integration with InferenceClient
  # ============================================

  Scenario: Use YOLO via InferenceClient detect_object method
    Given MLServer is running with a YOLO model
    And I have an InferenceClient configured with HttpOipAdapter
    When I call detect_object and provide an image
    Then I should receive an ObjectDetectionResult

  Scenario: Filter detections by confidence via InferenceClient
    Given MLServer is running with a YOLO model
    And I have an InferenceClient configured
    When I call detect_object with confidence threshold 0.7
    Then all returned detections should have confidence >= 0.7

  Scenario: Filter detections by label via InferenceClient
    Given MLServer is running with a YOLO model
    And I have an image with multiple object types
    When I call detect_object filtering for "person" label only
    Then all returned detections should have label "person"
