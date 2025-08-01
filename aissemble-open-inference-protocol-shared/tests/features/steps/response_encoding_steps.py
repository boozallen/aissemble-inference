from behave import given, when, then
import nose.tools as nt
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ResponseOutput,
    RequestOutput,
    Parameters,
    TensorData,
    Datatype,
)
from aissemble_open_inference_protocol_shared.codecs.utils import (
    build_inference_response,
)


@given('a handler returns output "{output_name}" with content type "{content_type}"')
def step_given_handler_output_with_content_type(context, output_name, content_type):
    output = ResponseOutput(
        name=output_name,
        shape=[1],
        datatype=Datatype.BYTES,
        parameters=Parameters(content_type=content_type),
        data=TensorData(root="handler-data"),
    )
    context.handler_response = InferenceResponse(
        model_name="test-model",
        outputs=[output],
    )


@given('a handler returns output "{output_name}" without content type')
def step_given_handler_output_without_content_type(context, output_name):
    output = ResponseOutput(
        name=output_name,
        shape=[1],
        datatype=Datatype.BYTES,
        parameters=Parameters(),
        data=TensorData(root="handler-data"),
    )
    context.handler_response = InferenceResponse(
        model_name="test-model",
        outputs=[output],
    )


@given('a request asks for output "{output_name}" with content type "{content_type}"')
def step_given_request_output_with_content_type(context, output_name, content_type):
    output = RequestOutput(
        name=output_name,
        parameters=Parameters(content_type=content_type),
    )
    context.request_outputs = [output]


@given('a request asks for content type "{content_type}" at request level')
def step_given_request_level_content_type(context, content_type):
    context.request_parameters = Parameters(content_type=content_type)


@when("the response is processed")
def step_when_response_processed(context):
    request = InferenceRequest(
        inputs=[],
        outputs=getattr(context, "request_outputs", None),
        parameters=getattr(context, "request_parameters", None),
    )
    context.response = build_inference_response(
        model_name="test-model",
        request=request,
        result=context.handler_response,
    )


@then('output "{output_name}" should use content type "{expected_content_type}"')
def step_then_output_should_use_content_type(
    context, output_name, expected_content_type
):
    found = False
    for output in context.response.outputs:
        if output.name == output_name:
            nt.eq_(
                output.parameters.content_type,
                expected_content_type,
                f'Output "{output_name}" content_type was "{output.parameters.content_type}", expected "{expected_content_type}"',
            )
            found = True
    nt.ok_(found, f"Output {output_name} not found in response")


@then('all outputs should use content type "{expected_content_type}"')
def step_then_all_outputs_should_use_content_type(context, expected_content_type):
    for output in context.response.outputs:
        nt.eq_(
            output.parameters.content_type,
            expected_content_type,
            f'Output "{output.name}" content_type was "{output.parameters.content_type}", expected "{expected_content_type}"',
        )
