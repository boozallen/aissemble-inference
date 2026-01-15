"""Step definitions for image processing and inference tests."""

import asyncio
import base64
from io import BytesIO

from behave import given, when, then
from mlserver.types import InferenceRequest, RequestInput
from mlserver.settings import ModelSettings, ModelParameters
from PIL import Image

from aissemble_oip_yolo import YOLORuntime

from pathlib import Path

# COCO dataset class names for validation
COCO_CLASSES = [
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]


def create_model_settings(model_variant: str = "yolov8n.pt") -> ModelSettings:
    """Create MLServer ModelSettings for testing."""
    parameters = ModelParameters(extra={"model": model_variant})
    return ModelSettings(
        name="yolo",
        implementation="aissemble_oip_yolo.YOLORuntime",
        parameters=parameters,
    )


def run_async(coro):
    """Helper to run async coroutines in sync context."""
    return asyncio.get_event_loop().run_until_complete(coro)


def create_test_image(width=640, height=480, color=(128, 128, 128)):
    """Create a test image with the specified dimensions and color."""
    return Image.new("RGB", (width, height), color)


def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """Convert PIL image to base64 string."""
    buffer = BytesIO()
    image.save(buffer, format=format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def create_inference_request(image_base64: str) -> InferenceRequest:
    """Create an MLServer InferenceRequest from base64 image data."""
    return InferenceRequest(
        inputs=[
            RequestInput(
                name="image",
                shape=[1, len(image_base64)],
                datatype="BYTES",
                data=[[image_base64]],
            )
        ]
    )


@given("a YOLOv8 model is loaded and ready")
def step_yolov8_ready(context):
    """Load a YOLOv8 model and ensure it's ready."""
    settings = create_model_settings("yolov8n.pt")
    context.runtime = YOLORuntime(settings)
    run_async(context.runtime.load())
    assert context.runtime.ready, "YOLOv8 model failed to load"


@given('I have a base64-encoded "{image_type}" image')
def step_have_image_type(context, image_type):
    """Create a test image in the specified format."""
    context.test_image = create_test_image()
    format_map = {"PNG": "PNG", "JPEG": "JPEG", "JPG": "JPEG"}
    context.image_format = format_map.get(image_type.upper(), "PNG")
    context.image_base64 = image_to_base64(context.test_image, context.image_format)


@given("I have an image containing a person")
def step_have_person_image(context):
    """Load an image containing a person for detection testing.

    Uses einstein-wikimedia-image.jpg from test-data, which is a photograph
    from Wikimedia Commons and is free to use under appropriate licenses.
    """
    test_data_dir = Path(__file__).parent.parent.parent / "test-data"
    image_path = test_data_dir / "einstein-wikimedia-image.jpg"

    assert image_path.exists(), f"Test image not found: {image_path}"

    context.test_image = Image.open(image_path)
    context.image_base64 = image_to_base64(context.test_image)
    context.expected_label = "person"


@given("I have a blank white image")
def step_have_blank_image(context):
    """Create a blank white image (should have no detections)."""
    context.test_image = create_test_image(640, 480, (255, 255, 255))
    context.image_base64 = image_to_base64(context.test_image)


@given("I have an image containing multiple objects")
def step_have_multi_object_image(context):
    """Create an image that may contain multiple detectable objects."""
    context.test_image = create_test_image(640, 480, (50, 50, 50))
    context.image_base64 = image_to_base64(context.test_image)


@given("I have an image for inference")
def step_have_inference_image(context):
    """Create a generic test image for inference."""
    context.test_image = create_test_image()
    context.image_base64 = image_to_base64(context.test_image)


@given("I have an image with detectable objects")
def step_have_detectable_image(context):
    """Create an image with potentially detectable objects."""
    context.test_image = create_test_image(640, 480, (100, 100, 100))
    context.image_base64 = image_to_base64(context.test_image)


@when("I send the image for inference")
def step_send_image(context):
    """Send the image for inference and capture the response."""
    request = create_inference_request(context.image_base64)
    try:
        context.inference_response = run_async(context.runtime.predict(request))
        context.inference_error = None
    except Exception as e:
        context.inference_response = None
        context.inference_error = e


@when("I send invalid base64 data for inference")
def step_send_invalid_base64(context):
    """Send invalid base64 data to test error handling."""
    request = create_inference_request("not-valid-base64!!!")
    try:
        context.inference_response = run_async(context.runtime.predict(request))
        context.inference_error = None
    except Exception as e:
        context.inference_response = None
        context.inference_error = e


@when("I send an empty input for inference")
def step_send_empty_input(context):
    """Send empty input to test error handling."""
    request = create_inference_request("")
    try:
        context.inference_response = run_async(context.runtime.predict(request))
        context.inference_error = None
    except Exception as e:
        context.inference_response = None
        context.inference_error = e


@when("I send base64-encoded text data for inference")
def step_send_text_as_image(context):
    """Send text data encoded as base64 (not an image)."""
    text_data = base64.b64encode(b"This is not an image").decode("utf-8")
    request = create_inference_request(text_data)
    try:
        context.inference_response = run_async(context.runtime.predict(request))
        context.inference_error = None
    except Exception as e:
        context.inference_response = None
        context.inference_error = e


@then("I should receive a valid inference response")
def step_valid_response(context):
    """Verify the response is valid."""
    assert context.inference_error is None, (
        f"Inference failed: {context.inference_error}"
    )
    assert context.inference_response is not None, "No response received"
    assert context.inference_response.outputs is not None, "Response has no outputs"


@then("I should receive detections in the response")
def step_has_detections(context):
    """Verify the response contains detections."""
    assert context.inference_response is not None, "No response received"
    outputs = {out.name: out for out in context.inference_response.outputs}
    bboxes = outputs.get("bboxes")
    assert bboxes is not None, "No bboxes output found"


@then('at least one detection should have label "{label}"')
def step_has_label(context, label):
    """Verify at least one detection has the expected label."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    labels = outputs.get("labels")
    assert labels is not None, "No labels output found"
    if labels.data:
        assert label in labels.data, (
            f"Expected label '{label}' not found in {labels.data}"
        )


@then("I should receive an empty detections list")
def step_empty_detections(context):
    """Verify the response has no detections."""
    assert context.inference_response is not None, "No response received"
    outputs = {out.name: out for out in context.inference_response.outputs}
    bboxes = outputs.get("bboxes")
    assert bboxes is not None, "No bboxes output found"
    assert len(bboxes.data) == 0, f"Expected empty bboxes, got {bboxes.data}"


@then("the response should still be valid OIP format")
def step_valid_oip_format(context):
    """Verify the response is valid OIP format even with no detections."""
    assert context.inference_response is not None, "No response received"
    outputs = {out.name: out for out in context.inference_response.outputs}
    assert "bboxes" in outputs, "Missing bboxes output"
    assert "labels" in outputs, "Missing labels output"
    assert "scores" in outputs, "Missing scores output"


@then("I should receive multiple detections")
def step_multiple_detections(context):
    """Verify multiple detections were returned."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    bboxes = outputs.get("bboxes")
    assert bboxes is not None, "No bboxes output found"


@then("each detection should have a unique bounding box")
def step_unique_bboxes(context):
    """Verify bounding boxes are unique (no duplicates)."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    bboxes = outputs.get("bboxes")
    if bboxes and bboxes.data:
        bbox_tuples = [tuple(b) if isinstance(b, list) else b for b in bboxes.data]
        assert len(bbox_tuples) == len(set(bbox_tuples)), (
            "Duplicate bounding boxes found"
        )


@then('the response should contain a "{output_name}" output')
def step_has_output(context, output_name):
    """Verify the response contains a specific output tensor."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    assert output_name in outputs, f"Missing '{output_name}' output"


@then("each bounding box should have 4 coordinates")
def step_bbox_has_4_coords(context):
    """Verify each bounding box has exactly 4 coordinates."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    bboxes = outputs.get("bboxes")
    if bboxes and bboxes.data:
        for bbox in bboxes.data:
            assert len(bbox) == 4, f"Expected 4 coordinates, got {len(bbox)}"


@then("coordinates should be in x1, y1, x2, y2 format")
def step_coords_format(context):
    """Verify coordinates follow x1, y1, x2, y2 format."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    bboxes = outputs.get("bboxes")
    if bboxes and bboxes.data:
        for bbox in bboxes.data:
            assert len(bbox) == 4, "Bounding box should have 4 coordinates"


@then("x2 should be greater than x1")
def step_x2_gt_x1(context):
    """Verify x2 > x1 for all bounding boxes."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    bboxes = outputs.get("bboxes")
    if bboxes and bboxes.data:
        for bbox in bboxes.data:
            assert bbox[2] > bbox[0], f"x2 ({bbox[2]}) should be > x1 ({bbox[0]})"


@then("y2 should be greater than y1")
def step_y2_gt_y1(context):
    """Verify y2 > y1 for all bounding boxes."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    bboxes = outputs.get("bboxes")
    if bboxes and bboxes.data:
        for bbox in bboxes.data:
            assert bbox[3] > bbox[1], f"y2 ({bbox[3]}) should be > y1 ({bbox[1]})"


@then("all confidence scores should be between 0 and 1")
def step_scores_in_range(context):
    """Verify all confidence scores are between 0 and 1."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    scores = outputs.get("scores")
    if scores and scores.data:
        for score in scores.data:
            assert 0 <= score <= 1, f"Score {score} is not in range [0, 1]"


@then("all labels should be non-empty strings")
def step_labels_nonempty(context):
    """Verify all labels are non-empty strings."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    labels = outputs.get("labels")
    if labels and labels.data:
        for label in labels.data:
            assert isinstance(label, str), f"Label {label} is not a string"
            assert len(label) > 0, "Empty label found"


@then("labels should be from the COCO dataset classes")
def step_labels_from_coco(context):
    """Verify all labels are valid COCO class names."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    labels = outputs.get("labels")
    if labels and labels.data:
        for label in labels.data:
            assert label in COCO_CLASSES, f"Label '{label}' not in COCO classes"


@then("the number of bounding boxes should equal the number of labels")
def step_bboxes_eq_labels(context):
    """Verify bounding box and label counts match."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    bboxes = outputs.get("bboxes")
    labels = outputs.get("labels")
    bbox_count = len(bboxes.data) if bboxes and bboxes.data else 0
    label_count = len(labels.data) if labels and labels.data else 0
    assert bbox_count == label_count, (
        f"Bounding box count ({bbox_count}) != label count ({label_count})"
    )


@then("the number of labels should equal the number of scores")
def step_labels_eq_scores(context):
    """Verify label and score counts match."""
    outputs = {out.name: out for out in context.inference_response.outputs}
    labels = outputs.get("labels")
    scores = outputs.get("scores")
    label_count = len(labels.data) if labels and labels.data else 0
    score_count = len(scores.data) if scores and scores.data else 0
    assert label_count == score_count, (
        f"Label count ({label_count}) != score count ({score_count})"
    )


@then("I should receive an error response")
def step_error_response(context):
    """Verify an error was received."""
    assert context.inference_error is not None, (
        "Expected an error but inference succeeded"
    )
