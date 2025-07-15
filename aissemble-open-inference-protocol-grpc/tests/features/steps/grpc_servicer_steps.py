import nose.tools as nt
from behave import given, when, then
from steps.handlers.test_dataplane_handler import (
    TestDataplaneHandler,
)

from aissemble_open_inference_protocol_grpc.grpc_inference_service_pb2 import (
    ModelInferRequest,
    InferTensorContents,
    InferParameter,
    ServerMetadataRequest,
    ModelMetadataRequest,
    ServerLiveRequest,
    ModelReadyRequest,
    ServerReadyRequest,
)
from aissemble_open_inference_protocol_grpc.inference_servicer import InferenceServicer
from aissemble_open_inference_protocol_shared.codecs.string import StringCodec
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceResponse,
    ResponseOutput,
    TensorData,
)
from aissemble_open_inference_protocol_grpc.mappers.model_inference_response_mapper import (
    ModelInferenceResponseMapper,
)

use_step_matcher("re")


@given("a handler to perform the request exists")
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


@given("the handler has model inferencing results")
def the_handler_has_model_inferencing_results(context):
    context.inference_response = InferenceResponse(
        model_name="test_model",
        model_version="123",
        id="test-id",
        outputs=[
            ResponseOutput(
                name="output-0",
                shape=[1, 3],
                datatype="INT64",
                data=TensorData(root=[1, 2, 3]),
                parameters={"content_type": "str"},
            )
        ],
    )


@given("a model metadata request exists")
def a_model_metadata_request_exists(context):
    context.model_metadata_request = ModelMetadataRequest(
        name="test_model", version="1.0"
    )


@given("a model ready request exists")
def a_model_ready_request_exists(context):
    context.model_ready_request = ModelReadyRequest(name="test_model", version="1.0")


@given("a server live request exists")
def a_server_live_request_exists(context):
    context.server_live_request = ServerLiveRequest()


@given("a server ready request exists")
def a_server_ready_request_exists(context):
    context.server_ready_request = ServerReadyRequest()


@given("a server metadata request exists")
def a_server_metadata_request_exists(context):
    context.server_metadata_request = ServerMetadataRequest()


@when("an infer request is sent to the gRPC servicer")
def an_infer_request_is_sent_to_the_gRPC_servicer(context):
    context.servicer_response = context.servicer.ModelInfer(
        request=context.model_infer_request, context=None
    )


@when("an infer response is sent to the handler")
def an_infer_response_is_sent_to_the_handler(context):
    inference_response_mapper = ModelInferenceResponseMapper()
    context.mapped_response = inference_response_mapper.to_model_inference_response(
        context.inference_response
    )


@when("the model metadata request is sent to the gRPC servicer")
def the_model_metadata_request_is_sent_to_the_gRPC_servicer(context):
    context.servicer_response = context.servicer.ModelMetadata(
        request=context.model_metadata_request, context=None
    )


@when("the model ready request is sent to the gRPC servicer")
def the_model_ready_request_is_sent_to_the_gRPC_servicer(context):
    context.servicer_response = context.servicer.ModelReady(
        request=context.model_ready_request, context=None
    )


@when("the server live request is sent to the gRPC servicer")
def the_server_live_request_is_sent_to_the_gRPC_servicer(context):
    context.servicer_response = context.servicer.ServerLive(
        request=context.server_live_request, context=None
    )


@when("the server ready request is sent to the gRPC servicer")
def the_server_ready_request_is_sent_to_the_gRPC_servicer(context):
    context.servicer_response = context.servicer.ServerReady(
        request=context.server_ready_request, context=None
    )


@when("the server metadata request is sent to the gRPC servicer")
def the_server_metadata_request_is_sent_to_the_gRPC_servicer(context):
    context.servicer_response = context.servicer.ServerMetadata(
        request=context.server_metadata_request, context=None
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
        expected_infer_request.parameters, actual_infer_request.parameters
    )
    _assert_inputs(expected_infer_request.inputs[0], actual_infer_request.inputs[0])
    _assert_infer_request_outputs(
        expected_infer_request.outputs[0], actual_infer_request.outputs[0]
    )


@then("the servicer's response corresponds to the handler's results")
def the_servicers_response_corresponds_to_the_handlers_results(context):
    actual_response = context.mapped_response
    expected_response = context.inference_response

    nt.eq_(
        actual_response.model_name,
        expected_response.model_name,
        "Model name did not match",
    )
    nt.eq_(
        actual_response.model_version,
        expected_response.model_version,
        "Model version did not match",
    )
    nt.eq_(actual_response.id, expected_response.id, "Request ID did not match")
    nt.eq_(
        len(actual_response.outputs),
        len(expected_response.outputs),
        "Number of outputs did not match",
    )

    _assert_infer_response_outputs(
        expected_response.outputs[0], actual_response.outputs[0]
    )


@then("the handler receives the model metadata request with the expected data")
def the_handler_receives_the_model_metadata_request_with_the_expected_data(context):
    expected_model_metadata_request = context.model_metadata_request
    nt.eq_(
        expected_model_metadata_request.name,
        context.handler.model_name,
        "Model name did not map correctly to the model metadata handler",
    )
    nt.eq_(
        expected_model_metadata_request.version,
        context.handler.model_version,
        "Model version did not map correctly to the model metadata handler",
    )


@then("the servicer's model metadata response corresponds to the handler's results")
def the_servicers_model_metadata_response_corresponds_to_the_handler_s_results(context):
    expected_model_metadata_response = context.handler.model_metadata_response
    actual_model_metadata_response = context.servicer_response
    nt.eq_(
        expected_model_metadata_response.name,
        actual_model_metadata_response.name,
        "Model name did not map correctly to the model metadata response",
    )
    nt.eq_(
        expected_model_metadata_response.versions,
        list(actual_model_metadata_response.versions),
        "Model version did not map correctly to the model metadata response",
    )
    nt.eq_(
        expected_model_metadata_response.platform,
        actual_model_metadata_response.platform,
        "Model version did not map correctly to the model metadata response",
    )

    # Test the mapping of the model metadata inputs
    nt.eq_(
        expected_model_metadata_response.inputs[0].name,
        actual_model_metadata_response.inputs[0].name,
        "Model metadata inputs name did not map correctly to the model metadata response",
    )
    nt.eq_(
        expected_model_metadata_response.inputs[0].datatype.value,
        actual_model_metadata_response.inputs[0].datatype,
        "Model metadata inputs datatype did not map correctly to the model metadata response",
    )
    nt.eq_(
        expected_model_metadata_response.inputs[0].shape,
        list(actual_model_metadata_response.inputs[0].shape),
        "Model metadata inputs shape did not map correctly to the model metadata response",
    )

    # Test the mapping of the model metadata outputs
    nt.eq_(
        expected_model_metadata_response.outputs[0].name,
        actual_model_metadata_response.outputs[0].name,
        "Model metadata outputs name did not map correctly to the model metadata response",
    )
    nt.eq_(
        expected_model_metadata_response.outputs[0].datatype.value,
        actual_model_metadata_response.outputs[0].datatype,
        "Model metadata outputs datatype did not map correctly to the model metadata response",
    )
    nt.eq_(
        expected_model_metadata_response.outputs[0].shape,
        list(actual_model_metadata_response.outputs[0].shape),
        "Model metadata outputs shape did not map correctly to the model metadata response",
    )


@then("the handler receives the model ready request with the expected data")
def the_handler_receives_the_model_ready_request_with_the_expected_data(context):
    expected_model_ready_request = context.model_ready_request
    nt.eq_(
        expected_model_ready_request.name,
        context.handler.model_name,
        "Model name did not map correctly to the model ready request",
    )
    nt.eq_(
        expected_model_ready_request.version,
        context.handler.model_version,
        "Model version did not map correctly to the model ready request",
    )


@then("the servicer's model ready response corresponds to the handler's results")
def the_servicers_model_ready_response_corresponds_to_the_handler_s_results(context):
    expected_model_ready_response = context.handler.model_ready_response
    actual_model_ready_response = context.servicer_response
    nt.eq_(
        expected_model_ready_response.ready,
        actual_model_ready_response.ready,
        "Model ready response did not map correctly",
    )


@then("the servicer's server metadata response corresponds to the handler's results")
def the_servicers_server_metadata_response_corresponds_to_the_handler_s_results(
    context,
):
    expected_server_metadata_response = context.handler.server_metadata_response
    actual_server_metadata_response = context.servicer_response
    nt.eq_(
        expected_server_metadata_response.name,
        actual_server_metadata_response.name,
        "Server name did not map correctly to the server metadata response",
    )
    nt.eq_(
        expected_server_metadata_response.version,
        actual_server_metadata_response.version,
        "Server version did not map correctly to the server metadata response",
    )
    nt.eq_(
        expected_server_metadata_response.extensions,
        actual_server_metadata_response.extensions,
        "Server extensions did not map correctly to the server metadata response",
    )


@then("the servicer's server ready response corresponds to the handler's results")
def the_servicers_server_ready_response_corresponds_to_the_handler_s_results(context):
    expected_server_ready_response = context.handler.server_ready_response
    actual_server_ready_response = context.servicer_response
    nt.eq_(
        expected_server_ready_response.live,
        actual_server_ready_response.ready,
        "Server ready response did not map correctly",
    )


@then("the servicer's server live response corresponds to the handler's results")
def the_servicers_server_live_response_corresponds_to_the_handler_s_results(context):
    expected_server_live_response = context.handler.server_live_response
    actual_server_live_response = context.servicer_response
    nt.eq_(
        expected_server_live_response.live,
        actual_server_live_response.live,
        "Server live response did not map correctly",
    )


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
        actual_infer_input.datatype.value,
        "Input datatype did not map correctly to inference request",
    )
    nt.eq_(
        expected_infer_input.shape,
        actual_infer_input.shape,
        "Input shape did not map correctly to inference request",
    )
    _assert_parameters(expected_infer_input.parameters, actual_infer_input.parameters)

    contents_descriptor, contents_value = expected_infer_input.contents.ListFields()[0]
    nt.eq_(
        list(contents_value),
        actual_infer_input.data.root,
        "Input content did not map correctly to inference request",
    )


def _assert_infer_request_outputs(
    expected_infer_request_outputs, actual_infer_request_outputs
):
    nt.eq_(
        expected_infer_request_outputs.name,
        actual_infer_request_outputs.name,
        "Output name did not map correctly to inference request",
    )
    _assert_parameters(
        expected_infer_request_outputs.parameters,
        actual_infer_request_outputs.parameters,
    )


def _assert_infer_response_outputs(
    expected_infer_response_output, actual_infer_response_output
):
    nt.eq_(
        actual_infer_response_output.name,
        expected_infer_response_output.name,
        "Output name did not match",
    )

    nt.eq_(
        actual_infer_response_output.shape,
        expected_infer_response_output.shape,
        "Output shape did not match",
    )

    field_descriptor, actual_value = actual_infer_response_output.contents.ListFields()[
        0
    ]

    expected_value = expected_infer_response_output.data.root
    nt.eq_(list(actual_value), expected_value, "Output tensor contents did not match")
