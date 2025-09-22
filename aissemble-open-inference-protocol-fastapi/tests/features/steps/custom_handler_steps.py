import nose.tools as nt
from behave import given, then, when
from fastapi.testclient import TestClient
from steps.handlers.handler_with_overridden_impl import (
    HandlerOverriddenImpl,
)
from steps.handlers.handler_without_optional_impl import (
    HandlerNoOptionalImpl,
)

from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import (
    AissembleOIPFastAPI,
)


@given(
    "custom implementation of model handler that doesn't implement the model ready method"
)
def given_custom_model_handler_without_optional_methods(context):
    api = AissembleOIPFastAPI(HandlerNoOptionalImpl())
    context.client = TestClient(api.server)


@given(
    "custom implementation of model handler that overrides implement the model ready method"
)
def given_custom_model_handler_overridden_methods(context):
    api = AissembleOIPFastAPI(HandlerOverriddenImpl())
    context.client = TestClient(api.server)


@when("model ready method is called")
def model_ready_method_is_called(context):
    context.header = None  # Anonymous
    send_method_request(context, "GET", "/v2/models/my_model/ready")


def send_method_request(context, method, path):
    context.response = context.client.request(
        method, path, json=None, headers=context.header
    )

    if "json" in context.response.headers.get("content-type", ""):
        context.schema = context.response.json()


@then("affirmative is responded")
def status_code_is_success(context):
    nt.ok_(
        context.response.status_code == 200,
        f"Expected status code 200, got {context.response.status_code}",
    )


@then("default logic is responded")
def default_logic_is_responded(context):
    str_content = context.response.content.decode("utf-8")
    nt.eq_(
        str_content,
        '{"name":"my_model","ready":true}',
        f"Default model_ready logic is expected but instead got {str_content}",
    )


@then("custom logic is responded")
def custom_logic_responded(context):
    str_content = context.response.content.decode("utf-8")
    nt.eq_(
        str_content,
        '{"name":"my_model","ready":false}',
        f"Custom model_ready logic is expected but instead got {str_content}",
    )
