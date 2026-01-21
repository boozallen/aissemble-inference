"""Step definitions for translator functionality tests."""

import base64
import os
import tempfile

from behave import given, when, then
from PIL import Image
import numpy as np

from aissemble_oip_core.client.oip_adapter import OipRequest, OipResponse, TensorData
from aissemble_oip_core.client.results import ObjectDetectionResult, Detection
from aissemble_oip_yolo import YOLOTranslator


def create_test_image(width=640, height=480, color=(128, 128, 128)):
    """Create a test image with the specified dimensions and color."""
    return Image.new("RGB", (width, height), color)


@given("I have a PIL Image object")
def step_have_pil_image(context):
    """Create a PIL Image object for testing."""
    context.test_input = create_test_image()
    context.translator = YOLOTranslator()


@given("I have a path to an image file")
def step_have_image_path(context):
    """Create a temporary image file and store its path."""
    image = create_test_image()
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    image.save(path)
    context.test_input = path
    context.temp_file_path = path
    context.translator = YOLOTranslator()


@given("I have a numpy array representing an image")
def step_have_numpy_array(context):
    """Create a numpy array representing an image."""
    context.test_input = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    context.translator = YOLOTranslator()


@given("I have a valid OipResponse with detections")
def step_have_oip_response_with_detections(context):
    """Create a mock OipResponse with detection data.

    Note: The translator expects data in specific formats:
    - bboxes: Either a flat list (reshapable to [N, 4]) or nested [[box1], [box2]]
    - labels/scores: Either flat list or nested [["label1", "label2"]]
    """
    context.oip_response = OipResponse(
        model_name="yolo",
        outputs=[
            TensorData(
                name="bboxes",
                shape=[2, 4],
                datatype="FP32",
                # Flat list format that will be reshaped to [2, 4]
                data=[10.0, 20.0, 100.0, 150.0, 200.0, 100.0, 300.0, 250.0],
            ),
            TensorData(
                name="labels",
                shape=[2],
                datatype="BYTES",
                data=["person", "car"],
            ),
            TensorData(
                name="scores",
                shape=[2],
                datatype="FP32",
                data=[0.95, 0.87],
            ),
        ],
        parameters={"_image_width": 640, "_image_height": 480},
    )
    context.translator = YOLOTranslator()


@given("I have a valid OipResponse with zero detections")
def step_have_oip_response_no_detections(context):
    """Create a mock OipResponse with no detections."""
    context.oip_response = OipResponse(
        model_name="yolo",
        outputs=[
            TensorData(
                name="bboxes",
                shape=[0, 4],
                datatype="FP32",
                data=[],
            ),
            TensorData(
                name="labels",
                shape=[0],
                datatype="BYTES",
                data=[],
            ),
            TensorData(
                name="scores",
                shape=[0],
                datatype="FP32",
                data=[],
            ),
        ],
        parameters={"_image_width": 640, "_image_height": 480},
    )
    context.translator = YOLOTranslator()


@when("I preprocess it with YOLOTranslator")
def step_preprocess_with_translator(context):
    """Preprocess the input with the translator."""
    try:
        context.oip_request = context.translator.preprocess(context.test_input)
        context.preprocess_error = None
    except Exception as e:
        context.oip_request = None
        context.preprocess_error = e


@when("I postprocess it with YOLOTranslator")
def step_postprocess_with_translator(context):
    """Postprocess the response with the translator."""
    try:
        context.detection_result = context.translator.postprocess(context.oip_response)
        context.postprocess_error = None
    except Exception as e:
        context.detection_result = None
        context.postprocess_error = e


@then("I should receive a valid OipRequest")
def step_valid_oip_request(context):
    """Verify a valid OipRequest was returned."""
    assert context.preprocess_error is None, (
        f"Preprocessing failed: {context.preprocess_error}"
    )
    assert context.oip_request is not None, "No OipRequest returned"
    assert isinstance(context.oip_request, OipRequest), (
        f"Expected OipRequest, got {type(context.oip_request)}"
    )
    assert len(context.oip_request.inputs) > 0, "OipRequest has no inputs"


@then("the request should contain base64-encoded image data")
def step_request_has_base64(context):
    """Verify the request contains base64-encoded image data."""
    assert context.oip_request is not None, "No OipRequest available"
    input_tensor = context.oip_request.inputs[0]
    assert input_tensor.datatype == "BYTES", (
        f"Expected BYTES datatype, got {input_tensor.datatype}"
    )
    image_data = input_tensor.data[0][0]
    try:
        decoded = base64.b64decode(image_data)
        assert len(decoded) > 0, "Decoded data is empty"
    except Exception as e:
        raise AssertionError(f"Data is not valid base64: {e}")


@then("I should receive an ObjectDetectionResult from the translator")
def step_receive_detection_result_from_translator(context):
    """Verify an ObjectDetectionResult was returned from the translator."""
    assert context.postprocess_error is None, (
        f"Postprocessing failed: {context.postprocess_error}"
    )
    assert context.detection_result is not None, "No result returned"
    assert isinstance(context.detection_result, ObjectDetectionResult), (
        f"Expected ObjectDetectionResult, got {type(context.detection_result)}"
    )


@then("the result should contain Detection objects")
def step_result_has_detections(context):
    """Verify the result contains Detection objects."""
    assert context.detection_result is not None, "No result available"
    assert len(context.detection_result.detections) > 0, "No detections in result"
    for detection in context.detection_result.detections:
        assert isinstance(detection, Detection), (
            f"Expected Detection, got {type(detection)}"
        )


@then("the result should have an empty detections list")
def step_result_empty_detections(context):
    """Verify the result has an empty detections list."""
    assert context.detection_result is not None, "No result available"
    assert len(context.detection_result.detections) == 0, (
        f"Expected empty detections, got {len(context.detection_result.detections)}"
    )
