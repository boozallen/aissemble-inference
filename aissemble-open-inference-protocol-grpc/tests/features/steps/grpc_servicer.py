import nose.tools as nt
from behave import *
from steps.handlers.test_dataplane_handler import (
    TestDataplaneHandler,
)

from aissemble_open_inference_protocol_grpc.grpcInferenceService_pb2 import (
    ModelInferRequest,
    InferTensorContents,
    InferParameter,
)
from aissemble_open_inference_protocol_grpc.inference_servicer import InferenceServicer
from aissemble_open_inference_protocol_shared.codecs.string import StringCodec

use_step_matcher("re")


@given("a handler to perform inferencing exists")
def a_handler_to_perform_inferencing_exists(context):
    context.handler = TestDataplaneHandler()


@given("an aissemble oip gRPC servicer exists with the handler")
def an_aissemble_oip_gRPC_servicer_exists_with_the_handler(context):
    context.servicer = InferenceServicer(handler=context.handler)


@given("an infer request exists")
def an_infer_request_exists(context):
    context.model_infer_request = ModelInferRequest(
        model_name="test_model",
        model_version="123",
        id="a test request",
        parameters={
            "my_bool_param": InferParameter(bool_param=True),
            "my_int64_param": InferParameter(int64_param=123),
            "my_string_param": InferParameter(string_param="some_param"),
            "my_double_param": InferParameter(double_param=1.1),
            "my_uint64_param": InferParameter(uint64_param=123),
        },
        inputs=[
            ModelInferRequest.InferInputTensor(
                name="input",
                datatype="INT64",
                shape=[1, 3],
                parameters={
                    "content_type": InferParameter(
                        string_param=StringCodec.ContentType
                    ),
                    "bool_param": InferParameter(bool_param=True),
                    "int64_param": InferParameter(int64_param=123),
                    "string_param": InferParameter(string_param="some_param"),
                    "double_param": InferParameter(double_param=1.1),
                    "uint64_param": InferParameter(uint64_param=123),
                },
                contents=InferTensorContents(int_contents=[1, 2, 3]),
            )
        ],
        outputs=[
            ModelInferRequest.InferRequestedOutputTensor(
                name="output",
                parameters={
                    "content_type": InferParameter(string_param=StringCodec.ContentType)
                },
            )
        ],
    )


@when("an infer request is sent to the gRPC servicer")
def an_infer_request_is_sent_to_the_gRPC_servicer(context):
    test = ModelInferRequest(
        id="",
        inputs=[
            ModelInferRequest.InferInputTensor(
                name="input-0",
                datatype="INT32",
                shape=[1, 3],
                parameters={"content_type": InferParameter(string_param="np")},
                contents=InferTensorContents(int_contents=[1, 2, 3]),
            )
        ],
    )

    context.servicer_response = context.servicer.ModelInfer(
        request=context.model_infer_request, context=None
    )


@then("the handler receives the request with the expected data")
def the_handler_receives_the_request_with_the_expected_data(context):
    expected_infer_request = context.model_infer_request
    actual_infer_request = context.handler.request_payload
    nt.assert_equal(
        expected_infer_request.model_name,
        context.handler.model_name,
        "Model name did not map correctly to inference request",
    )
    nt.assert_equal(
        expected_infer_request.model_version,
        context.handler.model_version,
        "Model version did not map correctly to inference request",
    )
    nt.assert_equal(
        expected_infer_request.id,
        actual_infer_request.id,
        "ID did not map correctly to inference request",
    )
    _assert_parameters(
        expected_infer_request.parameters, actual_infer_request.parameters[0]
    )
    _assert_inputs(expected_infer_request.inputs[0], actual_infer_request.inputs[0])
    _assert_outputs(expected_infer_request.outputs[0], actual_infer_request.outputs[0])


# TODO why are the params mapped to model_extra
def _assert_parameters(expected_infer_params, actual_infer_params):
    for model_field in actual_infer_params.model_fields_set:
        tensor_contents_fields = expected_infer_params[model_field].ListFields()
        field_descriptor, field_value = tensor_contents_fields[0]
        message = f"Did not find expected parameter or the expected value {model_field}"
        if model_field == "content_type":
            nt.eq_(field_value, actual_infer_params.content_type, message)
        else:
            nt.eq_(field_value, actual_infer_params.model_extra[model_field], message)


def _assert_inputs(expected_infer_input, actual_infer_input):
    nt.eq_(
        expected_infer_input.name,
        actual_infer_input.name,
        "Input name did not map correctly to inference request",
    )
    nt.eq_(
        expected_infer_input.datatype,
        actual_infer_input.datatype,
        "Input datatype did not map correctly to inference request",
    )
    nt.eq_(
        expected_infer_input.shape,
        actual_infer_input.shape,
        "Input shape did not map correctly to inference request",
    )
    _assert_parameters(
        expected_infer_input.parameters, actual_infer_input.parameters[0]
    )
    contents_descriptor, contents_value = expected_infer_input.contents.ListFields()[0]
    nt.eq_(
        contents_value,
        actual_infer_input.data.root[0],
        "Input content did not map correctly to inference request",
    )


def _assert_outputs(expected_infer_request_outputs, actual_infer_request_outputs):
    nt.eq_(
        expected_infer_request_outputs.name,
        actual_infer_request_outputs.name,
        "Output name did not map correctly to inference request",
    )
    _assert_parameters(
        expected_infer_request_outputs.parameters,
        actual_infer_request_outputs.parameters[0],
    )
