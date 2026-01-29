"""Behave environment configuration for sumy module tests.

This module provides setup and teardown hooks for behave test execution.
"""

from aissemble_inference_common_test.behave_helpers import (
    setup_mlserver_dynamic,
    start_mlserver_with_model as _start_mlserver_with_model,
    teardown_mlserver,
)


def before_all(context):
    """Execute before all tests run.

    Args:
        context: Behave context object
    """
    setup_mlserver_dynamic(context)


def before_scenario(context, scenario):
    """Execute before each scenario.

    Args:
        context: Behave context object
        scenario: Current scenario being executed
    """
    # Reset per-scenario state
    context.runtime = None
    context.load_result = None
    context.load_error = None
    context.inference_response = None
    context.inference_error = None
    context.oip_response = None
    context.summarization_result = None
    context.input_text = None


def after_scenario(context, scenario):
    """Execute after each scenario.

    Args:
        context: Behave context object
        scenario: Scenario that just completed
    """
    if hasattr(context, "mlserver_fixture") and context.mlserver_fixture.process:
        context.mlserver_fixture.stop()


def after_all(context):
    """Execute after all tests have run.

    Args:
        context: Behave context object
    """
    teardown_mlserver(context)


def start_mlserver_with_model(context, algorithm="textrank", sentences_count=3):
    """Start MLServer with specified Sumy model configuration.

    Args:
        context: Behave context
        algorithm: Summarization algorithm (textrank, lsa, lexrank)
        sentences_count: Number of sentences in summary
    """
    _start_mlserver_with_model(
        context,
        model_name="sumy",
        runtime="aissemble_inference_sumy.SumyRuntime",
        algorithm=algorithm,
        sentences_count=sentences_count,
        language="english",
    )
