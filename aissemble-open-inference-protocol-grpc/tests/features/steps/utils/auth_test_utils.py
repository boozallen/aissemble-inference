from unittest.mock import AsyncMock, Mock
from types import SimpleNamespace
from steps.handlers.test_dataplane_handler import TestDataplaneHandler
from aissemble_open_inference_protocol_grpc.inference_servicer import InferenceServicer
from aissemble_open_inference_protocol_grpc.grpc_inference_service_pb2 import (
    ModelInferRequest,
    InferTensorContents,
)

METHOD_NAME = "/test.inference.GRPCInferenceService/ModelInfer"


class AuthTestHelper:
    """Helper class for authorization testing with real servicer."""

    @staticmethod
    def create_mock_grpc_context(metadata):
        mock_context = Mock()
        mock_context.peer.return_value = "ipv4:127.0.0.1:12345"
        mock_context.invocation_metadata.return_value = metadata
        mock_context.abort = AsyncMock()
        return mock_context

    @staticmethod
    def create_test_servicer_and_handler():
        handler = TestDataplaneHandler()
        servicer = InferenceServicer(handler=handler)
        return servicer, handler

    @staticmethod
    def create_test_inference_request():
        return ModelInferRequest(
            model_name="test_model",
            model_version="123",
            id="auth_test_request",
            inputs=[
                ModelInferRequest.InferInputTensor(
                    name="input",
                    datatype="INT64",
                    shape=[1, 3],
                    contents=InferTensorContents(int_contents=[1, 2, 3]),
                )
            ],
            outputs=[
                ModelInferRequest.InferRequestedOutputTensor(
                    name="output",
                )
            ],
        )

    @staticmethod
    def create_intercepted_servicer_method(servicer, interceptor, method_name):
        original_method = getattr(servicer, method_name)

        # Create a wrapper that mimics the gRPC handler structure
        async def intercepted_method(request, context):
            # Create handler call details
            handler_call_details = Mock()
            handler_call_details.method = METHOD_NAME

            # Create the original handler wrapper
            def create_handler():
                return SimpleNamespace(
                    unary_unary=lambda req, ctx: original_method(req, ctx),
                    request_deserializer=None,
                    response_serializer=None,
                )

            continuation = AsyncMock(return_value=create_handler())

            # Apply interceptor
            wrapped_handler = await interceptor.intercept_service(
                continuation, handler_call_details
            )

            # Execute the intercepted method
            return await wrapped_handler.unary_unary(request, context)

        return intercepted_method
