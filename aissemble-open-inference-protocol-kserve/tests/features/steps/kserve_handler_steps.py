import nose.tools as nt
from behave import given, then, when
from kserve import InferRequest, InferInput, InferOutput
import asyncio

from handlers.test_dataplane_handler import TestDataPlaneHandler
from aissemble_open_inference_protocol_kserve.kserve_dataplane import (
    KServeDataplaneAdapter,
)

from aissemble_open_inference_protocol_shared.types.dataplane import Datatype


@given("KServeDataplaneHandler and CustomDataplaneHandler")
def given_kserve_and_custom_dataplane_handler(context):
    context.handler = TestDataPlaneHandler()
    context.kserve_dataplane_adapter = KServeDataplaneAdapter(handler=context.handler)


@when("model_ready is executed using the KServeDataplaneHandler")
def when_model_ready_using_kserve_dataplane_adapter(context):
    loop = asyncio.get_event_loop()
    context.result = loop.run_until_complete(
        context.kserve_dataplane_adapter.model_ready(model_name="test_model")
    )


@when("model_metadata is executed using the KServeDataplaneHandler")
def when_model_metadata_using_kserve_dataplane_adapter(context):
    loop = asyncio.get_event_loop()
    context.result = loop.run_until_complete(
        context.kserve_dataplane_adapter.model_metadata(model_name="test_model")
    )


@when("infer is executed using the KServeDataplaneHandler")
def when_infer_using_kserve_dataplane_adapter(context):
    infer_input = InferInput(
        name="input",
        shape=[1],
        datatype="FP32",
        data=[1.0, 2.0],
        parameters={},
    )
    infer_request = InferRequest(
        model_name="test",
        request_id="1",
        infer_inputs=[infer_input],
        from_grpc=False,
        model_version="v1",
    )
    loop = asyncio.get_event_loop()
    context.result = loop.run_until_complete(
        context.kserve_dataplane_adapter.infer(
            model_name="test_model", request=infer_request
        )
    )


@when("server_ready is executed using the KServeDataplaneHandler")
def when_server_ready_using_kserve_dataplane_adapter(context):
    loop = asyncio.get_event_loop()
    context.result = loop.run_until_complete(context.kserve_dataplane_adapter.ready())


@when("server_live is executed using the KServeDataplaneHandler")
def when_server_live_using_kserve_dataplane_adapter(context):
    loop = asyncio.get_event_loop()
    context.result = loop.run_until_complete(context.kserve_dataplane_adapter.live())


@when("server_metadata is executed using the KServeDataplaneHandler")
def when_server_metadata_using_kserve_dataplane_adapter(context):
    context.result = context.kserve_dataplane_adapter.metadata()


@then("CustomDataplaneHandler gets called to handle model_ready")
def custom_dataplane_handler_is_called_model_ready(context):
    nt.assert_true(context.handler.model_ready_called, "model_ready is called")


@then("model_ready is successful")
def model_ready_is_successful(context):
    nt.assert_true(context.result, "model should be ready")


@then("CustomDataplaneHandler gets called to handle model_metadata")
def custom_dataplane_handler_is_called_model_metadata(context):
    nt.assert_true(context.handler.model_metadata_called, "model_metadata is called")


@then("model_metadata is successful")
def model_metadata_is_successful(context):
    nt.assert_true(context.result, "model should be ready")
    model_inputs = [{"name": "input", "datatype": Datatype.FP32, "shape": [1]}]
    nt.assert_equal(
        context.result["name"],
        "test_model",
        "Model metadata is correctly showing model name",
    )
    nt.assert_equal(
        context.result["platform"],
        "python",
        "Model metadata is correctly showing platform",
    )
    nt.assert_equal(
        context.result["inputs"],
        model_inputs,
        "Model metadata is correctly showing inputs",
    )


@then("CustomDataplaneHandler gets called to handle infer")
def custom_dataplane_handler_is_called_infer(context):
    nt.assert_true(context.handler.infer_called, "infer is called")


@then("infer is successful")
def infer_is_successful(context):
    nt.assert_equal(
        context.result[0].id,
        "1",
        "Model Infer is correctly showing model id",
    )
    nt.assert_equal(
        context.result[0].model_name,
        "test_model",
        "Model Infer is correctly showing model name",
    )
    nt.assert_equal(
        context.result[0].outputs,
        [
            InferOutput(
                name="test_model",
                shape=[1],
                datatype="FP32",
                data=[1, 2, 3],
            )
        ],
        "Model Infer is correctly showing model name",
    )


@then("CustomDataplaneHandler gets called to handle server_ready")
def custom_dataplane_handler_is_called_server_ready(context):
    nt.assert_true(context.handler.server_ready_called, "server_ready is called")


@then("server_ready is successful")
def server_ready_is_successful(context):
    nt.assert_true(context.result, "Server should be ready")


@then("CustomDataplaneHandler gets called to handle server_live")
def custom_dataplane_handler_is_called_server_live(context):
    nt.assert_true(context.handler.server_live_called, "server_live is called")


@then("server_live is successful")
def server_live_is_successful(context):
    nt.assert_equal(
        context.result,
        {"status": "alive"},
        "Server should be live",
    )


@then("CustomDataplaneHandler gets called to handle server_metadata")
def custom_dataplane_handler_is_called_server_metadata(context):
    nt.assert_true(context.handler.server_metadata_called, "server_metadata is called")


@then("server_metadata is successful")
def server_metadata_is_successful(context):
    nt.assert_equal(
        context.result,
        {
            "name": "Inference Server",
            "version": "1.0",
            "extensions": [],
        },
        "Server should be live",
    )
