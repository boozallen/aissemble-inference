from behave import given, when, then
import nose.tools as nt
import ast
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    RequestInput,
    Parameters,
    RequestOutput,
    InferenceResponse,
    ResponseOutput,
)
from aissemble_open_inference_protocol_shared.codecs.utils import (
    encode_inference_response,
    encode_response_output,
    decode_inference_request,
)

# this import statement instantiates and registers the StringCodec
import aissemble_open_inference_protocol_shared.codecs.string  # noqa: F401


@given(
    "an InferenceRequest with string content_type at the request level and payload {payload}"
)
def step_given_request_level(context, payload):
    data = ast.literal_eval(payload)
    context.expected = data
    input_obj = RequestInput(
        name="input-0",
        datatype="BYTES",
        shape=[len(data), 1],
        data=data,
        parameters=Parameters(),
    )
    context.inference_request = InferenceRequest(
        model_name="test-model",
        inputs=[input_obj],
        parameters=Parameters(content_type="str"),
    )


@given(
    "an InferenceRequest with string content_type at the input level and payload {payload}"
)
def step_given_input_level(context, payload):
    data = ast.literal_eval(payload)
    context.expected = data
    input_obj = RequestInput(
        name="input-0",
        datatype="BYTES",
        shape=[len(data), 1],
        data=data,
        parameters=Parameters(content_type="str"),
    )
    context.inference_request = InferenceRequest(
        model_name="test-model",
        inputs=[input_obj],
        parameters=Parameters(),
    )


@given("a payload with type string {payload}")
def step_given_payload(context, payload):
    context.payload = ast.literal_eval(payload)


@when("the payload is decoded")
def step_when_decode(context):
    context.result = decode_inference_request(context.inference_request)


@when("the payload is encoded at the response level")
def step_when_encode_response(context):
    context.result = encode_inference_response(
        model_name="test-model", payload=context.payload
    )


@when("the payload is encoded at the request level")
def step_when_encode_request(context):
    request_output = RequestOutput(
        name="output-0",
        parameters=Parameters(content_type="str"),
    )
    context.result = encode_response_output(context.payload, request_output)


@then("the result should be a list of strings matching {expected}")
def step_then_list_match(context, expected):
    expected_list = ast.literal_eval(expected)
    # If decode_inference_request returned a list, compare directly
    if isinstance(context.result, list):
        nt.ok_(
            context.result == expected_list,
            f"Expected {expected_list}, got {context.result}",
        )
    # If it returned an InferenceRequest, extract the data
    elif hasattr(context.result, "inputs"):
        actual = []
        for input in context.result.inputs:
            if hasattr(input.data, "root"):
                actual = input.data.root
        nt.ok_(actual == expected_list, f"Expected {expected_list}, got {actual}")
    else:
        nt.ok_(False, f"Unexpected result type: {type(context.result)}")


@then("the result should be an InferenceResponse")
def step_then_inference_response(context):
    nt.ok_(
        isinstance(context.result, InferenceResponse),
        f"Expected InferenceResponse. Got {type(context.result)}",
    )


@then("the result should be a ResponseOutput")
def step_then_response_output(context):
    nt.ok_(
        isinstance(context.result, ResponseOutput),
        f"Expected ResponseOutput. Got {type(context.result)}",
    )
