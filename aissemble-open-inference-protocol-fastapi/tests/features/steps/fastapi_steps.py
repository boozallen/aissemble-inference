from behave import given, then, when
from fastapi.testclient import TestClient
from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import (
    AissembleOIPFastAPI,
)


@given("I have an OIP FastAPI app with the default handler")
def given_i_have_fastapi_app(context):
    api = AissembleOIPFastAPI()
    context.client = TestClient(api.app)


@when('I send a "{method}" request to "{path}"')
def when_i_send_a_method_request(context, method, path):
    context.header = None  # Anonymous
    send_method_request(context, method, path)


@when('I send a "{method}" request to "{path}" with an authorization header')
def send_method_request_with_header(context, method, path):
    context.header = {"Authorization": f"Bearer {context.jwt}"}
    send_method_request(context, method, path)


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


@then("the response status code should be {code:d}")
def status_code_is(context, code):
    assert context.response.status_code == code


@then('the response should contain "{message}"')
def step_impl(context, message):
    assert message in context.response.text


@then('the schema contains a "{method}" path for "{route}"')
def schema_contains_method_and_route(context, method, route):
    assert route in context.schema["paths"], f"{route} not in OpenAPI paths"
    assert method in context.schema["paths"][route], f"{method} not in {route} path"
