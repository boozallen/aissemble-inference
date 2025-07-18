from typing import Optional

from aissemble_open_inference_protocol_shared.handlers.dataplane import DataplaneHandler
from aissemble_open_inference_protocol_shared.types.dataplane import (
    ModelReadyResponse,
    ModelMetadataResponse,
    InferenceRequest,
    InferenceResponse,
    ResponseOutput,
    Datatype,
    Parameters,
    TensorData,
)


class TestHandler(DataplaneHandler):
    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        output1 = ResponseOutput(
            name="output-1",
            shape=[1],
            datatype=Datatype.BYTES,
            parameters=Parameters(content_type="str"),
            data=TensorData(root=b"byte output data"),
        )
        output2 = ResponseOutput(
            name="output-2",
            shape=[1, 3],
            datatype=Datatype.INT64,
            data=TensorData(root=[1, 2, 3]),
        )
        return InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            id=payload.id,
            outputs=[output1, output2],
        )

    def model_metadata(
        self, model_name: str, model_version: Optional[str] = None
    ) -> ModelMetadataResponse:
        # No test currently using method
        pass

    def model_ready(
        self, model_name: str, model_version: Optional[str] = None
    ) -> ModelReadyResponse:
        # No test currently using method
        pass
