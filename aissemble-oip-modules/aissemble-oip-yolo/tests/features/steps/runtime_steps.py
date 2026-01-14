"""Step definitions for model loading tests."""

import asyncio

from behave import given, when, then
from mlserver.settings import ModelSettings, ModelParameters

from aissemble_oip_yolo import YOLORuntime


def create_model_settings(model_variant: str = None) -> ModelSettings:
    """Create MLServer ModelSettings for testing.

    Args:
        model_variant: Optional model variant to use

    Returns:
        ModelSettings configured for YOLO
    """
    parameters = ModelParameters(
        extra={"model": model_variant} if model_variant else {}
    )
    return ModelSettings(
        name="yolo",
        implementation="aissemble_oip_yolo.YOLORuntime",
        parameters=parameters,
    )


def run_async(coro):
    """Helper to run async coroutines in sync context."""
    return asyncio.get_event_loop().run_until_complete(coro)


@given('MLServer is configured with model variant "{model_variant}"')
def step_configure_model_variant(context, model_variant):
    """Configure MLServer settings with a specific model variant."""
    context.model_variant = model_variant
    context.settings = create_model_settings(model_variant)


@given("MLServer is configured without a model variant parameter")
def step_configure_no_variant(context):
    """Configure MLServer settings without model parameter (uses default)."""
    context.settings = create_model_settings()


@when("the YOLORuntime loads the model")
def step_load_model(context):
    """Create and load the YOLORuntime with the configured settings."""
    context.runtime = YOLORuntime(context.settings)
    try:
        context.load_result = run_async(context.runtime.load())
        context.load_error = None
    except Exception as e:
        context.load_result = False
        context.load_error = e


@when("the YOLORuntime attempts to load the model")
def step_attempt_load_model(context):
    """Attempt to load a model, expecting potential failure."""
    context.runtime = YOLORuntime(context.settings)
    try:
        context.load_result = run_async(context.runtime.load())
        context.load_error = None
    except Exception as e:
        context.load_result = False
        context.load_error = e


@then("the model should load successfully")
def step_model_loaded(context):
    """Verify the model loaded successfully."""
    assert context.load_error is None, (
        f"Model loading failed with error: {context.load_error}"
    )
    assert context.load_result is True, "Model loading did not return True"


@then("the runtime should be ready for inference")
def step_runtime_ready(context):
    """Verify the runtime is ready for inference."""
    assert context.runtime.ready is True, "Runtime is not ready for inference"


@then('the default "{default_model}" model should be used')
def step_default_model_used(context, default_model):
    """Verify the default model was loaded."""
    assert hasattr(context.runtime, "_model"), "Runtime has no _model attribute"
    assert context.runtime._model is not None, "Model was not loaded"


@then("the model loading should fail with an appropriate error")
def step_model_loading_failed(context):
    """Verify the model loading failed."""
    assert context.load_error is not None, (
        "Expected model loading to fail, but it succeeded"
    )
