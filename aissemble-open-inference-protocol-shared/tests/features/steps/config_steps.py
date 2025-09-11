import os
import sys
from types import NoneType

from behave import given, when, then
from krausening.properties import PropertyManager

from aissemble_open_inference_protocol_shared.config.oip_config import OIPConfig


@given("no config overrides are provided")
def step_no_config_overrides(context):
    # Testing default functionality
    pass


@given("the configs are set via krausening properties")
def step_krausening_configs(context):
    # The properties file location
    os.environ["KRAUSENING_BASE"] = "tests/resources/krausening/base"

    pm = PropertyManager.get_instance()
    pm.get_properties("oip.properties", force_reload=True)


@given("the configs are set via environment variables")
def step_env_configs(context):
    os.environ["KSERVE_GRPC_PORT"] = "7070"
    os.environ["KSERVE_WORKERS"] = "2"
    os.environ["FASTAPI_PORT"] = "9082"
    os.environ["GRPC_HOST"] = "10.0.0.1"
    os.environ["AUTH_ALGORITHM"] = "RS256"
    os.environ["OIP_PDP_URL"] = "http://test:8080/pdp"


@given("the configs are set via kserve arguments")
def step_kserve_args_configs(context):
    # Save original for cleanup
    context.original_argv = sys.argv.copy()

    # Set sys.argv with the KServe arguments
    sys.argv = [sys.argv[0]] + [
        "--http_port",
        "9080",
        "--grpc_port",
        "9081",
        "--workers",
        "3",
        "--max_threads",
        "8",
        "--max_asyncio_workers",
        "2",
        "--enable_grpc",
        "false",
        "--enable_docs_url",
        "true",
        "--enable_latency_logging",
        "false",
        "--access_log_format",
        "arg-log-format",
    ]


@given(
    "kserve_http_port has krausening {krausening_value}, env {env_value}, and args {arg_value}"
)
def step_given_kserve_http_port_config(context, krausening_value, env_value, arg_value):
    # Save original sys.argv for cleanup
    context.original_argv = sys.argv.copy()

    # Set environment variable if provided (not empty string)
    if env_value and env_value != "None":
        os.environ["KSERVE_HTTP_PORT"] = env_value

    # Set command line argument if provided (not empty string)
    if arg_value and arg_value != "None":
        sys.argv = [sys.argv[0], "--http_port", arg_value]

    # Note: krausening_value is documented but not set (already in properties file)


@when("I create an OIPConfig instance")
def step_create_config(context):
    context.oip_config = OIPConfig()


@then("the following configuration values should be returned")
def step_verify_defaults(context):
    for row in context.table:
        config_name = row["config"]
        expected_value_str = row["expected_value"]
        verify_config_value(context.oip_config, config_name, expected_value_str)


@then("the configuration {config} should have value {expected_value}")
def step_verify_single_config_value(context, config, expected_value):
    verify_config_value(context.oip_config, config, expected_value)


def verify_config_value(oip_config, config_name, expected_value_str):
    """Helper function to verify a single configuration value."""
    # Get the attribute
    attr = getattr(oip_config, config_name)

    # Check if it's a method or a property
    if callable(attr):
        actual_value = attr()
    else:
        actual_value = attr

    # Parse expected value to correct type
    parsed_expected = _parse_expected_value(expected_value_str, actual_value)

    assert actual_value == parsed_expected, (
        f"Expected {config_name} to be {parsed_expected}, but got {actual_value}"
    )


def _parse_expected_value(exp_value: str, act_value: str):
    """Helper function to convert string values from the feature table to appropriate Python types."""
    act_value_type = type(act_value)

    if act_value_type is NoneType:
        return None
    elif act_value_type is bool:
        return exp_value == "True"
    elif act_value_type is int:
        return int(exp_value)
    else:
        return exp_value
