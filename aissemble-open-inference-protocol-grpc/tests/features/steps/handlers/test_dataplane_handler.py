from typing import Optional

from aissemble_open_inference_protocol_shared.handlers.dataplane import DataplaneHandler
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelReadyResponse,
    ModelMetadataResponse,
    ResponseOutput,
)


class TestDataplaneHandler(DataplaneHandler):
    def __init__(self):
        self.model_version = None
        self.model_name = None
        self.request_payload = None
        self.inference_response = None

    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        self.request_payload = payload
        self.model_name = model_name
        self.model_version = model_version

        response_output = ResponseOutput(
            name=payload.inputs[0].name,
            shape=payload.inputs[0].shape,
            datatype=payload.inputs[0].datatype,
            data=payload.inputs[0].data,
        )
        self.inference_response = InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            id=payload.id,
            outputs=[response_output],
            parameters=payload.parameters,
        )
        return self.inference_response

    def model_metadata(
        self, model_name: str, model_version: Optional[str] = None
    ) -> ModelMetadataResponse:
        pass

    def model_ready(
        self, model_name: str, model_version: Optional[str] = None
    ) -> ModelReadyResponse:
        pass
