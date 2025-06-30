###
# #%L
# aiSSEMBLE::Open Inference Protocol::gRPC
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import grpc
from krausening.logging import LogManager

from aissemble_open_inference_protocol_grpc.grpcInferenceService_pb2 import (
    ModelInferResponse,
)
from aissemble_open_inference_protocol_grpc.grpcInferenceService_pb2_grpc import (
    GRPCInferenceServiceServicer,
)
from aissemble_open_inference_protocol_grpc.mappers.model_inference_request_mapper import (
    ModelInferenceRequestMapper,
)


class InferenceServicer(GRPCInferenceServiceServicer):
    logger = LogManager.get_instance().get_logger("InferenceServicer")

    def __init__(self, handler):
        self.handler = handler

    def ModelInfer(self, request, context) -> ModelInferResponse:
        """The ModelInfer API performs inference using the specified model. Errors are
        indicated by the google.rpc.Status returned for the request. The OK code
        indicates success and other codes indicate failure.
        """
        self.logger.info("Received Model Inference request")
        try:
            model_inference_request_mapper = ModelInferenceRequestMapper()
            inference_request = model_inference_request_mapper.to_inference_request(
                request
            )
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal Server Error!")
            raise ModelInferenceRequestMapper.MappingException("Internal Server Error!")

        try:
            self.logger.info("Sending model inference request to the handler")
            # Send request to handler
            handler_response = self.handler.infer(
                payload=inference_request,
                model_name=request.model_name,
                model_version=request.model_version,
            )

            # TODO convert InferenceResponse to ModelInferResponse
            return ModelInferResponse(
                model_name=request.model_name,
                model_version=handler_response.model_version,
                id=request.id,
                outputs=[],
            )
        except Exception:
            context.set_code(grpc.StatusCode.UNIMPLEMENTED)
            context.set_details("Method not implemented!")
            raise NotImplementedError("Method not implemented!")
