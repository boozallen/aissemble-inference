from behave import given, when, then
import nose.tools as nt
import ast
import numpy as np

from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    RequestInput,
    Parameters,
    RequestOutput,
    InferenceResponse,
    ResponseOutput,
    Datatype,
)
from aissemble_open_inference_protocol_shared.codecs.utils import (
    decode_inference_request,
    encode_inference_response,
    encode_response_output,
)

# importing registers the numpy codec
import aissemble_open_inference_protocol_shared.codecs.numpy  # noqa: F401


@given(
    "an InferenceRequest with numpy content_type at the request level and payload {payload}"
)
def step_given_request_level_numpy(context, payload):
    data = ast.literal_eval(payload)
    context.expected = np.array(data)
    shape = list(context.expected.shape)
    input_obj = RequestInput(
        name="input-0",
        datatype=Datatype.INT64,
        shape=shape,
        data=data,
        parameters=Parameters(),
    )
    context.inference_request = InferenceRequest(
        inputs=[input_obj],
        parameters=Parameters(content_type="numpy"),
    )


@given(
    "an InferenceRequest with numpy content_type at the request level and multi-dimensional payload {payload}"
)
def step_given_request_level_numpy_multidimensional(context, payload):
    data = ast.literal_eval(payload)
    np_data = np.array(data)
    context.expected = np_data
    shape = list(np_data.shape)
    input_obj = RequestInput(
        name="input-0",
        datatype=Datatype.INT64,
        shape=shape,
        data=data,
        parameters=Parameters(),
    )
    context.inference_request = InferenceRequest(
        inputs=[input_obj],
        parameters=Parameters(content_type="numpy"),
    )


@given(
    "an InferenceRequest with numpy content_type at the input level and payload {payload}"
)
def step_given_input_level_numpy(context, payload):
    data = ast.literal_eval(payload)
    context.expected = np.array(data)
    shape = list(context.expected.shape)
    input_obj = RequestInput(
        name="input-0",
        datatype=Datatype.INT64,
        shape=shape,
        data=data,
        parameters=Parameters(content_type="numpy"),
    )
    context.inference_request = InferenceRequest(
        inputs=[input_obj],
        parameters=Parameters(),
    )


@given(
    "an InferenceRequest with numpy content_type at the input level and multiple numpy inputs"
)
def step_given_multiple_numpy_inputs(context):
    # create two inputs
    data1 = [1, 2, 3]
    data2 = [4, 5, 6]
    context.expected = [np.array(data1), np.array(data2)]
    shape1 = list(np.array(data1).shape)
    shape2 = list(np.array(data2).shape)
    input1 = RequestInput(
        name="input-0",
        datatype=Datatype.INT64,
        shape=shape1,
        data=data1,
        parameters=Parameters(content_type="numpy"),
    )
    input2 = RequestInput(
        name="input-1",
        datatype=Datatype.INT64,
        shape=shape2,
        data=data2,
        parameters=Parameters(content_type="numpy"),
    )
    context.inference_request = InferenceRequest(
        inputs=[input1, input2],
        parameters=Parameters(),
    )


@given("a payload with type numpy {payload}")
def step_given_numpy_payload(context, payload):
    context.payload = np.array(ast.literal_eval(payload))


@when("the numpy payload is decoded")
def step_when_decode_numpy_inputs(context):
    context.result = decode_inference_request(context.inference_request)


@when("I encode the payload at the response level")
def step_when_encode_numpy_response(context):
    context.result = encode_inference_response(
        model_name="test-model", payload=context.payload
    )


@when("I encode the payload at the request level")
def step_when_encode_numpy_request(context):
    request_output = RequestOutput(
        name="output-0", parameters=Parameters(content_type="numpy")
    )
    context.result = encode_response_output(context.payload, request_output)


@then("the result should be a numpy array matching {expected}")
def step_then_numpy_match(context, expected):
    expected_arr = np.array(ast.literal_eval(expected))
    result = context.result
    # If result is an InferenceRequest, extract the data
    if hasattr(result, "inputs"):
        result = np.array(result.inputs[0].data.root)
    nt.ok_(
        np.array_equal(result, expected_arr),
        f"Expected {expected_arr}, got {result}",
    )


@then("the result should be a multiple outputs with type numpy array")
def step_then_multiple_outputs(context):
    result = context.result
    # If result is an InferenceRequest, extract the data as a list of numpy arrays
    if hasattr(result, "inputs"):
        result = [np.array(inp.data.root) for inp in result.inputs]
    for arr, expected in zip(result, context.expected):
        nt.ok_(
            np.array_equal(arr, expected),
            f"Expected {expected}, got {arr}",
        )


@then("the result should be a numpy InferenceResponse")
def step_then_numpy_inference_response(context):
    nt.ok_(
        isinstance(context.result, InferenceResponse),
        f"Expected InferenceResponse, got {type(context.result)}",
    )


@then("the result should be a numpy ResponseOutput")
def step_then_numpy_response_output(context):
    nt.ok_(
        isinstance(context.result, ResponseOutput),
        f"Expected ResponseOutput, got {type(context.result)}",
    )
