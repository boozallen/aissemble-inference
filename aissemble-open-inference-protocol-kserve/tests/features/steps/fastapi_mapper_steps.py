from behave import given, then, when
import nose.tools as nt
from kserve import InferRequest, InferInput, InferResponse, InferOutput
from aissemble_open_inference_protocol_shared.types.dataplane import (
    Parameters,
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    RequestOutput,
    ResponseOutput,
    Datatype,
    TensorData,
)
from kserve.protocol.infer_type import RequestedOutput

from aissemble_open_inference_protocol_kserve.mappers.infer_mapper import (
    InferMapper,
)


@given("an InferRequest with KServe")
def given_infer_request_with_kserve(context):
    infer_input = InferInput(
        name="input",
        shape=[1],
        datatype="FP32",
        data=[1, 2],
        parameters=Parameters(),
    )
    infer_output = RequestedOutput(
        name="output",
        parameters=Parameters(),
    )
    context.infer_request = InferRequest(
        model_name="test",
        request_id="1",
        infer_inputs=[infer_input],
        from_grpc=False,
        parameters={},
        model_version="v1",
        request_outputs=[infer_output],
    )


@given("an InferenceResponse with the dataplane handler")
def given_inference_response_with_fastapi(context):
    infer_output = ResponseOutput(
        name="output",
        shape=[1],
        datatype=Datatype.FP32,
        data=[11, 22],
        parameters=Parameters(),
    )
    context.inference_response = InferenceResponse(
        model_name="output",
        model_version="v1",
        id="1",
        parameters=Parameters(),
        outputs=[infer_output],
    )


@when(
    "InferRequest for KServe is converted to InferenceRequest for the dataplane handler"
)
def when_i_send_convert_inference_request(context):
    context.result = InferMapper.infer_request_to_inference_request(
        context.infer_request
    )


@when(
    "InferenceResponse for the dataplane handler is converted to InferResponse for KServe"
)
def when_i_send_convert_infer_response(context):
    context.result = InferMapper.inference_response_to_infer_response(
        context.inference_response
    )


@then("InferenceRequest is correctly returned")
def inference_request_correctly_returned(context):
    request_input = RequestInput(
        name="input",
        shape=[1],
        datatype=Datatype.FP32,
        parameters=Parameters(),
        data=TensorData(root=[1, 2]),
    )

    request_output = RequestOutput(name="output", parameters=Parameters())

    expected_inference_request = InferenceRequest(
        id="1",
        parameters=Parameters(),
        inputs=[request_input],
        outputs=[request_output],
    )
    nt.assert_equal(
        expected_inference_request.id,
        context.result.id,
        "Model id did not map correctly to InferenceRequest",
    )

    nt.assert_equal(
        expected_inference_request.parameters,
        context.result.parameters,
        "Model parameters did not map correctly to InferenceRequest",
    )

    nt.assert_equal(
        expected_inference_request.inputs[0].data,
        context.result.inputs[0].data,
        "Model input data did not map correctly to InferenceRequest",
    )

    nt.assert_equal(
        expected_inference_request.inputs[0].datatype,
        context.result.inputs[0].datatype,
        "Model input datatype did not map correctly to InferenceRequest",
    )

    nt.assert_equal(
        expected_inference_request.inputs[0].shape,
        context.result.inputs[0].shape,
        "Model input shape did not map correctly to InferenceRequest",
    )

    nt.assert_equal(
        expected_inference_request.outputs[0].name,
        context.result.outputs[0].name,
        "Model output name did not map correctly to InferenceRequest",
    )


@then("InferResponse is correctly returned")
def infer_response_correctly_returned(context):
    infer_output = InferOutput(
        name="output",
        shape=[1],
        datatype="FP32",
        data=[11, 22],
        parameters=Parameters(),
    )

    expected_infer_response = InferResponse(
        response_id="1",
        model_name="output",
        infer_outputs=[infer_output],
        model_version="v1",
        parameters=Parameters(),
        from_grpc=False,
    )
    nt.assert_equal(
        expected_infer_response.id,
        context.result.id,
        "Model id did not map correctly to InferResponse",
    )

    nt.assert_equal(
        expected_infer_response.model_name,
        context.result.model_name,
        "Model name did not map correctly to InferResponse",
    )

    nt.assert_equal(
        expected_infer_response.parameters,
        context.result.parameters,
        "Model parameters did not map correctly to InferResponse",
    )

    nt.assert_equal(
        expected_infer_response.outputs[0].data,
        context.result.outputs[0].data,
        "Model output data did not map correctly to InferResponse",
    )

    nt.assert_equal(
        expected_infer_response.outputs[0].datatype,
        context.result.outputs[0].datatype,
        "Model output datatype did not map correctly to InferResponse",
    )

    nt.assert_equal(
        expected_infer_response.outputs[0].shape,
        context.result.outputs[0].shape,
        "Model output shape did not map correctly to InferResponse",
    )

    nt.assert_equal(
        expected_infer_response.from_grpc,
        context.result.from_grpc,
        "Model is grpc flag did not map correctly to InferResponse",
    )
