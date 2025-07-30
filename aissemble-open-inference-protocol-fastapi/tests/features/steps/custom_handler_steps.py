import nose.tools as nt

from behave import given, then, when
from fastapi.testclient import TestClient
from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import (
    AissembleOIPFastAPI,
)
from steps.handler_without_required_impl import (
    HandlerNoImpl,
)

from steps.handler_without_optional_impl import (
    HandlerNoOptionalImpl,
)

from steps.handler_with_overridden_impl import (
    HandlerOverriddenImpl,
)


@given(
    "custom implementation of dataplane handler that doesn't implement required methods"
)
def given_custom_handler_without_required_methods(context):
    api = AissembleOIPFastAPI(HandlerNoImpl)
    context.client = TestClient(api.server)


@given(
    "custom implementation of dataplane handler that doesn't implement server methods"
)
def given_custom_handler_without_optional_methods(context):
    api = AissembleOIPFastAPI(HandlerNoOptionalImpl)
    context.client = TestClient(api.server)


@given(
    "custom implementation of dataplane handler that override implement server methods"
)
def given_custom_handler_overridden_methods(context):
    api = AissembleOIPFastAPI(HandlerOverriddenImpl)
    context.client = TestClient(api.server)


@when("model method is called")
def when_i_send_a_method_request(context):
    context.header = None  # Anonymous
    send_method_request_with_exception_handle(
        context, "POST", "/v2/models/my_model/infer"
    )


@when("server status method is called")
def when_i_send_a_server_ready_method_request(context):
    context.header = None  # Anonymous
    send_method_request(context, "GET", "/v2/health/ready")


def send_method_request(context, method, path):
    payload = None
    headers = context.header
    if method.upper() == "POST" and "infer" in path:
        # Create a payload for POST /infer requests; FastAPI returns 422 Unprocessable Entity if no JSON body is sent
        payload = {"inputs": []}
    context.response = context.client.request(
        method, path, json=payload, headers=headers
    )

    if "json" in context.response.headers.get("content-type", ""):
        context.schema = context.response.json()


def send_method_request_with_exception_handle(context, method, path):
    try:
        payload = None
        headers = context.header
        if method.upper() == "POST" and "infer" in path:
            # Create a payload for POST /infer requests; FastAPI returns 422 Unprocessable Entity if no JSON body is sent
            payload = {"inputs": []}
        context.response = context.client.request(
            method, path, json=payload, headers=headers
        )

        if "json" in context.response.headers.get("content-type", ""):
            context.schema = context.response.json()
    except Exception as ex:
        context.exception = ex


@then("Error is raised")
def status_code_is_error(context):
    assert isinstance(context.exception, TypeError)


@then("affirmative is responded")
def status_code_is_success(context):
    nt.ok_(
        context.response.status_code == 200,
        f"Expected status code 200, got {context.response.status_code}",
    )


@then("custom logic is reponded")
def custom_logic_responded(context):
    str_content = context.response.content.decode("utf-8")
    assert str_content == '{"live":false}'
