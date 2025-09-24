from typing import Optional

from aissemble_open_inference_protocol_shared.handlers.dataplane import (
    DataplaneHandler,
)
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelReadyResponse,
    ModelMetadataResponse,
    ResponseOutput,
    MetadataTensor,
    Datatype,
    ServerMetadataResponse,
    ServerLiveResponse,
    ServerReadyResponse,
)


class TestDataplaneHandler(DataplaneHandler):
    def __init__(self):
        super().__init__()
        self.model_version = None
        self.model_name = None
        self.request_payload = None
        self.inference_response = None
        self.model_metadata_response = None
        self.model_ready_response = None
        self.server_ready_response = None
        self.server_live_response = None
        self.server_metadata_response = None

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
        self.model_name = model_name
        self.model_version = model_version
        model_input_tensor = [
            MetadataTensor(name="input", datatype=Datatype.INT64, shape=[1, 1])
        ]
        model_output_tensor = [
            MetadataTensor(name="output", datatype=Datatype.FP64, shape=[1, 1])
        ]
        self.model_metadata_response = ModelMetadataResponse(
            name=model_name,
            versions=["1.0", "2.0", "3.0"],
            platform="GPU",
            inputs=model_input_tensor,
            outputs=model_output_tensor,
        )
        return self.model_metadata_response

    def model_ready(
        self, model_name: str, model_version: Optional[str] = None
    ) -> ModelReadyResponse:
        self.model_name = model_name
        self.model_version = model_version
        self.model_ready_response = ModelReadyResponse(name=model_name, ready=True)
        return self.model_ready_response

    def server_metadata(self) -> ServerMetadataResponse:
        self.server_metadata_response = ServerMetadataResponse(
            name="Model Server", version="1.0", extensions=["v2"]
        )
        return self.server_metadata_response

    def server_ready(self) -> ServerReadyResponse:
        self.server_ready_response = ServerReadyResponse(live=True)
        return self.server_ready_response

    def server_live(self) -> ServerLiveResponse:
        self.server_live_response = ServerLiveResponse(live=True)
        return self.server_live_response

    def model_load(self, model_name) -> bool:
        return True
