"""Step definitions for InferenceClient integration tests."""

import base64
import sys
from io import BytesIO
from pathlib import Path

from behave import given, when, then
from PIL import Image

from aissemble_inference_core.client import InferenceClient
from aissemble_inference_core.client.oip_adapter import HttpOipAdapter
from aissemble_inference_core.client.results import ObjectDetectionResult


def _get_start_mlserver_func():
    """Lazily import start_mlserver_with_model from environment.py."""
    features_dir = Path(__file__).parent.parent
    if str(features_dir) not in sys.path:
        sys.path.insert(0, str(features_dir))
    from environment import start_mlserver_with_model

    return start_mlserver_with_model


def create_test_image(width=640, height=480, color=(128, 128, 128)):
    """Create a test image with the specified dimensions and color."""
    return Image.new("RGB", (width, height), color)


def image_to_base64(image: Image.Image) -> str:
    """Convert PIL image to base64 string."""
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


@given("MLServer is running with a YOLO model")
def step_mlserver_running(context):
    """Start MLServer with a YOLO model."""
    start_mlserver = _get_start_mlserver_func()
    start_mlserver(context, model_variant="yolov8n.pt")


@given("I have an InferenceClient configured with HttpOipAdapter")
def step_have_inference_client(context):
    """Create an InferenceClient with HTTP adapter."""
    adapter = HttpOipAdapter(context.mlserver_url, "yolo")
    context.client = InferenceClient(adapter, context.mlserver_url)
    context.adapter = adapter


@given("I have an InferenceClient configured")
def step_have_inference_client_simple(context):
    """Create an InferenceClient with HTTP adapter."""
    if not hasattr(context, "mlserver_url") or context.mlserver_url is None:
        start_mlserver = _get_start_mlserver_func()
        start_mlserver(context, model_variant="yolov8n.pt")
    adapter = HttpOipAdapter(context.mlserver_url, "yolo")
    context.client = InferenceClient(adapter, context.mlserver_url)
    context.adapter = adapter


@given("I have an image with multiple object types")
def step_have_multi_type_image(context):
    """Create an image that may contain multiple object types."""
    context.test_image = create_test_image(640, 480, (100, 100, 100))


@when("I call detect_object and provide an image")
def step_call_detect_object(context):
    """Call detect_object with an image."""
    test_image = create_test_image()
    try:
        context.detection_result = (
            context.client.detect_object("yolo").image(test_image).run()
        )
        context.detection_error = None
    except Exception as e:
        context.detection_result = None
        context.detection_error = e


@when("I call detect_object with confidence threshold {threshold}")
def step_call_detect_with_confidence(context, threshold):
    """Call detect_object with a confidence threshold."""
    test_image = create_test_image()
    threshold_float = float(threshold)
    try:
        context.detection_result = (
            context.client.detect_object("yolo")
            .image(test_image)
            .confidence(threshold_float)
            .run()
        )
        context.detection_error = None
        context.confidence_threshold = threshold_float
    except Exception as e:
        context.detection_result = None
        context.detection_error = e


@when('I call detect_object filtering for "{label}" label only')
def step_call_detect_with_label_filter(context, label):
    """Call detect_object with label filtering."""
    try:
        context.detection_result = (
            context.client.detect_object("yolo")
            .image(context.test_image)
            .labels([label])
            .run()
        )
        context.detection_error = None
        context.filter_label = label
    except Exception as e:
        context.detection_result = None
        context.detection_error = e


@then("I should receive an ObjectDetectionResult")
def step_receive_object_detection_result(context):
    """Verify an ObjectDetectionResult was returned."""
    if context.detection_error:
        raise AssertionError(f"Detection failed: {context.detection_error}")
    assert context.detection_result is not None, "No result received"
    assert isinstance(context.detection_result, ObjectDetectionResult), (
        f"Expected ObjectDetectionResult, got {type(context.detection_result)}"
    )


@then("all returned detections should have confidence >= {threshold}")
def step_all_detections_above_threshold(context, threshold):
    """Verify all detections meet the confidence threshold."""
    threshold_float = float(threshold)
    if context.detection_result and context.detection_result.detections:
        for detection in context.detection_result.detections:
            assert detection.confidence >= threshold_float, (
                f"Detection confidence {detection.confidence} < threshold {threshold_float}"
            )


@then('all returned detections should have label "{label}"')
def step_all_detections_have_label(context, label):
    """Verify all detections have the expected label."""
    if context.detection_result and context.detection_result.detections:
        for detection in context.detection_result.detections:
            assert detection.label == label, (
                f"Detection label '{detection.label}' != expected '{label}'"
            )
