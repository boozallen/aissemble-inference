"""Behave environment for summarization example tests."""

from pathlib import Path

from aissemble_oip_common_test.behave_helpers import (
    setup_mlserver_simple,
    teardown_mlserver,
)


def before_all(context):
    """Start MLServer before running tests."""
    example_dir = Path(__file__).parent.parent.parent
    models_dir = example_dir / "models"

    setup_mlserver_simple(context, models_dir=models_dir, port=8080)
    context.mlserver_fixture.start()

    # Update context attributes for backward compatibility
    context.mlserver_url = context.mlserver_fixture.url
    context.mlserver_port = context.mlserver_fixture.port
    context.mlserver_process = context.mlserver_fixture.process

    # Set test data directory
    context.test_data_dir = example_dir / "tests" / "test_data"


def after_all(context):
    """Stop MLServer after all tests complete."""
    teardown_mlserver(context)
