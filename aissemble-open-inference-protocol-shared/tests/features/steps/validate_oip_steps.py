from behave import given, when, then
import ast
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    ResponseOutput,
    Datatype,
    TensorData,
    flatten,
    validate_shape,
    validate_datatype,
    shape_is_valid,
)

DATAPLANE_CLASSES = {
    "ResponseOutput": ResponseOutput,
    "RequestInput": RequestInput,
    "InferenceRequest": InferenceRequest,
    "InferenceResponse": InferenceResponse,
}


@given("a {request_response} whose shape is {expected_shape}")
def step_given_request_response_shape(context, request_response, expected_shape):
    context.request_response = DATAPLANE_CLASSES[request_response]
    context.expected_shape = ast.literal_eval(expected_shape)


@given("a {request_response} whose datatype is {expected_datatype}")
def step_given_request_response_datatype(context, request_response, expected_datatype):
    context.request_response = DATAPLANE_CLASSES[request_response]
    context.expected_datatype = Datatype[expected_datatype]


@given("a data field whose value is {actual_data}")
def step_given_data(context, actual_data):
    data = ast.literal_eval(actual_data)

    # sets shape and datatype using context property if it exists, otherwise use defaults given
    shape = getattr(
        context, "expected_shape", [] if not isinstance(data, list) else [len(data)]
    )
    datatype = getattr(context, "expected_datatype", Datatype.BYTES)

    context.instance = context.request_response(
        name="test-0",
        shape=shape,
        datatype=datatype,
        data=TensorData(root=data),
    )


@when("the {request_response} shape is validated")
def step_when_the_request_response_shape_is_validated(context, request_response):
    try:
        validate_shape(context.instance.shape, context.instance.data.root)
        context.validation_result = "successful"
    except Exception as e:
        context.validation_result = "unsuccessful"
        context.exception = e


@when("the {request_response} datatype is validated")
def step_when_the_request_response_datatype_is_validated(context, request_response):
    try:
        flat_data = flatten(context.instance.data.root)
        validate_datatype(context.instance.datatype, flat_data)
        context.validation_result = "successful"
    except Exception as e:
        context.validation_result = "unsuccessful"
        context.exception = e


@then("the validation is {result}")
def step_then_validation_result(context, result):
    expected_result = result.strip('"')
    actual_result = context.validation_result

    assert actual_result == expected_result, (
        f"Expected validation to be '{expected_result}', but got '{actual_result}'"
    )


@given(
    "an {inference_request_response} with name {name}, shape {expected_shape}, datatype {expected_datatype}, and data {actual_data}"
)
def step_given_inference_request_response(
    context,
    inference_request_response,
    name,
    expected_shape,
    expected_datatype,
    actual_data,
):
    context.inference_request_response = DATAPLANE_CLASSES[inference_request_response]
    shape = ast.literal_eval(expected_shape)
    datatype = Datatype(expected_datatype)
    data = ast.literal_eval(actual_data)

    if inference_request_response == "InferenceRequest":
        request_input = RequestInput(
            name=name, shape=shape, datatype=datatype, data=TensorData(root=data)
        )
        context.instance = context.inference_request_response(inputs=[request_input])
    else:
        response_output = ResponseOutput(
            name=name, shape=shape, datatype=datatype, data=TensorData(root=data)
        )
        context.instance = context.inference_request_response(
            model_name="test-model", outputs=[response_output]
        )


@when("the {inference_request_response} is validated")
def step_the_inference_request_response_is_validated(
    context, inference_request_response
):
    try:
        context.instance.validate_oip()
        context.validation_result = "successful"
    except Exception as e:
        context.validation_result = "unsuccessful"
        context.exception = e


@given("an input shape of {actual_data} is given and {desired_shape} is desired")
def step_an_input_shape_of_is_given_and_is_desired(
    context,
    actual_data,
    desired_shape,
):
    context.actual_data = ast.literal_eval(actual_data)
    context.desired_shape = ast.literal_eval(desired_shape)


@when("the input shape validation is performed")
def step_input_shape_validation_is_performed(context):
    context.shape_validity = shape_is_valid(context.desired_shape, context.actual_data)


@then("the shape validation is {valid}")
def step_the_shape_validation_is_valid(context, valid):
    valid = valid.strip().lower() == "true"
    assert context.shape_validity == valid, (
        f"Expected validation to be '{valid}', but got '{context.shape_validity}'"
    )
