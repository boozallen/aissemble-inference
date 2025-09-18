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
    ResponseOutput,
)
from handlers.test_handler import TestHandler
import re


@given("I have an OIP FastAPI app with the default handler")
def given_i_have_fastapi_app(context):
    api = AissembleOIPFastAPI()
    context.client = TestClient(api.server)


@given("I have a handler that returns outputs data")
def i_have_a_handler_that_returns_outputs_data(context):
    context.handler = TestHandler()


@given("I have an OIP FastAPI app with the handler")
def i_have_an_oip_fast_api_app_with_the_handler(context):
    api = AissembleOIPFastAPI(context.handler)
    context.client = TestClient(api.server)
    context.api = api


@given("I have an infer request")
def i_have_an_infer_request(context):
    create_inference_request(context)


@given('inference request has "{data}" with "{shape}" and "{datatype}"')
def inference_request_has_data_with_shape_and_datatype(context, data, shape, datatype):
    context.input = get_request_input(
        name="invalid-input-test",
        shape=json.loads(shape),
        datatype=Datatype(datatype),
        data=json.loads(data),
    )


@given('inference response has "{data}" with "{shape}" and "{datatype}"')
def inference_response_has_data_with_shape_and_datatype(context, data, shape, datatype):
    context.handler.response_output = ResponseOutput(
        name="invalid-output-test",
        shape=json.loads(shape),
        datatype=Datatype(datatype),
        data=TensorData(root=json.loads(data)),
    )
    context.output = RequestOutput(name="invalid-output-test")


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
        create_inference_request(context)
        payload = get_json_str(context.request_payload)
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


def create_inference_request(context):
    context.request_payload = InferenceRequest(id="test request", inputs=[], outputs=[])

    if hasattr(context, "input"):
        context.request_payload.id = "test inference request validation"
        context.request_payload.inputs.append(context.input)
    else:
        context.request_payload.inputs.append(get_request_input(name="input-1"))

    if hasattr(context, "output"):
        context.request_payload.id = "test inference response validation"
        context.request_payload.outputs.append(context.output)
    else:
        _output1 = RequestOutput(
            name="output-1", parameters=Parameters(content_type="str")
        )
        _output2 = RequestOutput(name="output-2")
        context.request_payload.outputs.append(_output1)
        context.request_payload.outputs.append(_output2)


def get_json_str(obj):
    content = f"{obj.inputs[0].data.root}"
    if content == "some data":
        replaced_content = f'"{content}"'
    else:
        content = replaced_content = f"{content}".replace("[", "").replace("]", "")

    json_str = json.dumps(obj, default=lambda o: o.__dict__)
    # update the generated json str to match the expected json format for data
    json_str = re.sub(
        r'"data":\s+\{"root":\s+("|\[)' + content + '("|\])\}',
        r'"data": [' + replaced_content + "]",
        json_str,
    )
    return json_str


def get_request_input(name, shape=[1], datatype=Datatype.BYTES, data="some data"):
    return RequestInput(
        name=name,
        shape=shape,
        datatype=datatype,
        data=TensorData(root=data),
    )
