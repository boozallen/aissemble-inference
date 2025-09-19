from typing import Optional

from tensorflow.keras.models import load_model

from aissemble_open_inference_protocol_shared.handlers.dataplane import (
    DataplaneHandler,
)

from aissemble_open_inference_protocol_shared.types.dataplane import (
    Datatype,
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelReadyResponse,
    MetadataTensor,
    ResponseOutput,
    ServerReadyResponse,
    ServerLiveResponse,
    ServerMetadataResponse,
    TensorData,
)


class TestDataPlaneHandler(DataplaneHandler):
    def __init__(self):
        super().__init__()
        self.ready = False
        self.model = None
        # Those variables are to test whether method below is called
        self.model_load_called = None
        self.model_ready_called = None
        self.model_metadata_called = None
        self.infer_called = None
        self.server_ready_called = None
        self.server_live_called = None
        self.server_metadata_called = None

    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        output_list = TensorData(root=[1, 2, 3])
        self.infer_called = True
        return InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            id=payload.id,
            outputs=[
                ResponseOutput(
                    name=model_name,
                    shape=payload.inputs[0].shape,
                    datatype=Datatype.FP32,
                    data=output_list,
                )
            ],
        )

    def model_metadata(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        input_tensors = []
        inputmtensor = MetadataTensor(name="input", datatype=Datatype.FP32, shape=[1])
        input_tensors.append(inputmtensor)
        output_tensors = []
        outputmtensor = MetadataTensor(name="output", datatype=Datatype.FP32, shape=[1])
        output_tensors.append(outputmtensor)

        self.model_metadata_called = True

        return ModelMetadataResponse(
            name=model_name,
            versions=[model_version] if model_version else None,
            platform="python",
            inputs=input_tensors,
            outputs=output_tensors,
        )

    def model_ready(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelReadyResponse:
        self.model_ready_called = True
        return ModelReadyResponse(name=model_name, ready=True)

    def model_load(self, model_name) -> bool:
        self.model = load_model("tests/resources/" + model_name + ".keras")
        self.ready = True
        self.model_load_called = True
        return True

    def server_ready(self) -> ServerReadyResponse:
        self.server_ready_called = True
        return ServerReadyResponse(live=True)

    def server_live(self) -> ServerLiveResponse:
        self.server_live_called = True
        return ServerLiveResponse(live=True)

    def server_metadata(self) -> ServerMetadataResponse:
        self.server_metadata_called = True
        return ServerMetadataResponse(
            name="Inference Server", version="1.0", extensions=[]
        )
