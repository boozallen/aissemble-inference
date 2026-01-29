"""Step definitions for object detection tests."""

import os

from behave import given, then, when
from PIL import Image, ImageDraw

from aissemble_inference_core.client.inference_client import InferenceClient
from aissemble_inference_core.client.oip_adapter import HttpOipAdapter


@given("MLServer is running with the YOLOv8 model")
def step_mlserver_running(context):
    """Verify MLServer is running (handled by environment.py)."""
    assert hasattr(context, "mlserver_url"), "MLServer URL not set"


@given("I have an image containing common objects")
def step_have_image(context):
    """Create or load a test image with detectable objects."""
    test_data_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "test_data"
    )
    context.test_image_path = os.path.join(test_data_dir, "test_image.png")

    if not os.path.exists(context.test_image_path):
        _create_test_image(context.test_image_path)

    assert os.path.exists(context.test_image_path), "Test image not found"


@when("I run object detection using the OIP client")
def step_run_detection(context):
    """Run object detection using the OIP client."""
    adapter = HttpOipAdapter(
        base_url=context.mlserver_url,
        model_name="yolov8",
    )
    client = InferenceClient(adapter=adapter, endpoint=context.mlserver_url)

    context.result = client.detect_object().image(context.test_image_path).run()


@when("I run object detection with a confidence threshold of {threshold:f}")
def step_run_detection_with_threshold(context, threshold):
    """Run object detection with a confidence threshold."""
    adapter = HttpOipAdapter(
        base_url=context.mlserver_url,
        model_name="yolov8",
    )
    client = InferenceClient(adapter=adapter, endpoint=context.mlserver_url)

    context.result = (
        client.detect_object()
        .image(context.test_image_path)
        .confidence(threshold)
        .run()
    )
    context.confidence_threshold = threshold


@then("I should receive detection results")
def step_receive_results(context):
    """Verify that detection results were returned."""
    assert context.result is not None, "No results returned"


@then("the results should contain bounding boxes")
def step_results_contain_bboxes(context):
    """Verify results contain bounding boxes."""
    if len(context.result.detections) > 0:
        detection = context.result.detections[0]
        assert detection.bbox is not None, "No bounding box in detection"
        assert detection.bbox.x1 is not None, "Bounding box missing x1"
        assert detection.bbox.y1 is not None, "Bounding box missing y1"
        assert detection.bbox.x2 is not None, "Bounding box missing x2"
        assert detection.bbox.y2 is not None, "Bounding box missing y2"


@then("the results should contain labels")
def step_results_contain_labels(context):
    """Verify results contain labels."""
    if len(context.result.detections) > 0:
        detection = context.result.detections[0]
        assert detection.label is not None, "No label in detection"
        assert isinstance(detection.label, str), "Label is not a string"


@then("the results should contain confidence scores")
def step_results_contain_scores(context):
    """Verify results contain confidence scores."""
    if len(context.result.detections) > 0:
        detection = context.result.detections[0]
        assert detection.confidence is not None, "No confidence in detection"
        assert 0 <= detection.confidence <= 1, "Confidence not in valid range"


@then("all returned detections should have confidence above {threshold:f}")
def step_all_above_threshold(context, threshold):
    """Verify all detections are above the threshold."""
    for detection in context.result.detections:
        assert detection.confidence >= threshold, (
            f"Detection confidence {detection.confidence} below threshold {threshold}"
        )


def _create_test_image(path: str):
    """Create a simple test image with geometric shapes.

    YOLOv8 is trained on COCO dataset and may not detect simple shapes,
    but this ensures the pipeline works end-to-end. For more reliable
    detection, use a real photograph.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    img = Image.new("RGB", (640, 480), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.rectangle([100, 100, 250, 250], fill=(255, 0, 0), outline=(0, 0, 0))
    draw.ellipse([300, 100, 450, 250], fill=(0, 255, 0), outline=(0, 0, 0))
    draw.polygon(
        [(550, 250), (475, 100), (625, 100)], fill=(0, 0, 255), outline=(0, 0, 0)
    )

    img.save(path, "PNG")
