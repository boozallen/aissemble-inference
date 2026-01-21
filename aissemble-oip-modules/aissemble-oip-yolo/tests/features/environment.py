"""Behave environment hooks for YOLO module tests."""

from aissemble_oip_common_test.behave_helpers import (
    setup_mlserver_dynamic,
    start_mlserver_with_model as _start_mlserver_with_model,
    teardown_mlserver,
)


def before_all(context):
    """Initialize test context."""
    setup_mlserver_dynamic(context)


def before_scenario(context, scenario):
    """Reset per-scenario state."""
    context.model_variant = None
    context.runtime = None
    context.load_result = None
    context.load_error = None
    context.inference_response = None
    context.inference_error = None
    context.oip_request = None
    context.oip_response = None
    context.detection_result = None
    context.test_image = None
    context.test_image_path = None


def after_scenario(context, scenario):
    """Clean up after each scenario."""
    if hasattr(context, "mlserver_fixture") and context.mlserver_fixture.process:
        context.mlserver_fixture.stop()


def after_all(context):
    """Final cleanup."""
    teardown_mlserver(context)


def start_mlserver_with_model(context, model_variant=None):
    """Start MLServer with specified YOLO model configuration.

    Args:
        context: Behave context
        model_variant: Model variant to configure (e.g., "yolov8n.pt")
    """
    _start_mlserver_with_model(
        context,
        model_name="yolo",
        runtime="aissemble_oip_yolo.YOLORuntime",
        model=model_variant,
    )
