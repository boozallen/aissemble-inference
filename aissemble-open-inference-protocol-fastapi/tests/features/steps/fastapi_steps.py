from behave import given, then, when
import nose.tools as nt
import json
from fastapi.testclient import TestClient
from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import (
    AissembleOIPFastAPI,
)
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    RequestInput,
    Datatype,
    Parameters,
    TensorData,
    RequestOutput,
)
from handlers.test_handler import TestHandler


@given("I have an OIP FastAPI app with the default handler")
def given_i_have_fastapi_app(context):
    api = AissembleOIPFastAPI()
    context.client = TestClient(api.server)


@given("I have a handler that returns outputs data")
def i_have_a_handler_that_returns_outputs_data(context):
    context.handler = TestHandler


@given("I have an OIP FastAPI app with the handler")
def i_have_an_oip_fast_api_app_with_the_handler(context):
    api = AissembleOIPFastAPI(context.handler)
    context.client = TestClient(api.server)
    context.api = api


@given("I have an infer request")
def i_have_an_infer_request(context):
    _input = RequestInput(
        name="input-1",
        shape=[1],
        datatype=Datatype.BYTES,
        data=TensorData(root="some data"),
    )
    _output1 = RequestOutput(name="output-1", parameters=Parameters(content_type="str"))
    _output2 = RequestOutput(name="output-2")
    context.request_payload = InferenceRequest(
        id="test request", inputs=[_input], outputs=[_output1, _output2]
    )


@when('I send a "{method}" request to "{path}"')
def when_i_send_a_method_request(context, method, path):
    context.header = None  # Anonymous
    send_method_request(context, method, path)


@when('I send a "{method}" request to "{path}" with an authorization header')
def send_method_request_with_header(context, method, path):
    context.header = {"Authorization": f"Bearer {context.jwt}"}
    send_method_request(context, method, path)


def send_method_request(context, method, path):
    headers = context.header
    if method.upper() == "POST" and "infer" in path:
        # Create a payload for POST /infer requests; JSON body must be sent
        if hasattr(context, "request_payload"):
            payload = json.dumps(context.request_payload, default=lambda o: o.__dict__)
        else:
            payload = json.dumps(
                InferenceRequest(id="test request", inputs=[]),
                default=lambda o: o.__dict__,
            )
        context.response = context.client.request(
            method, path, content=payload, headers=headers
        )
    else:
        context.response = context.client.request(method, path, headers=headers)

    if "json" in context.response.headers.get("content-type", ""):
        context.schema = context.response.json()


@then("the response status code should be {code:d}")
def status_code_is(context, code):
    nt.eq_(code, context.response.status_code, f"Status code should be {code}")


@then('the response should contain "{message}"')
def step_impl(context, message):
    nt.ok_(
        message in context.response.text,
        f"Response did not contain expected message: {message}",
    )


@then('the schema contains a "{method}" path for "{route}"')
def schema_contains_method_and_route(context, method, route):
    nt.ok_(route in context.schema["paths"], f"{route} not in OpenAPI paths")
    nt.ok_(method in context.schema["paths"][route], f"{method} not in {route} path")
