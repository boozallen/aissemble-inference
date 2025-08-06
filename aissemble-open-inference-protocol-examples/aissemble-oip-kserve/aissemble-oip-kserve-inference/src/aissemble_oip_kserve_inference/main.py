###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples KServe Inference
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from kserve import ModelServer
import numpy as np
from typing import Optional
from tensorflow.keras.models import load_model

from krausening.logging import LogManager

from aissemble_open_inference_protocol_kserve.aissemble_oip_kserve import (
    AissembleOIPKServe,
)

from aissemble_open_inference_protocol_shared.handlers.dataplane import DataplaneHandler
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelReadyResponse,
    MetadataTensor,
    ResponseOutput,
    Datatype,
)

""""
AissembleOIPKServe is base class for Kserve Handler that implements predict method. (Other methods will be implemented soon) 
If user wants to use what AissembleOIPKServe offers there is no need to create custom class and we can just make AissembleOIPKServe instance. 
If user somehow wants to implement custom logic for prediction or load, user can extend AissembleOIPKServe with custom logic to override it.
In this case, only load is overridden and predict method will be used from AissembleOIPKServe class
"""


class customFastAPIHandler(DataplaneHandler):
    def __init__(self):
        super().__init__()

    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        # Model will take input data from the payload and make prediction to convert Celsius to Fahrenheit.
        output = self.model.predict(np.array(payload.inputs[0].data))
        # Need to convert to list so that we are align with output format.
        output_list = output.tolist()

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
        model = load_model("model/" + model_name + ".keras")

        input_tensors = []
        for input in model.inputs:
            datatype = None
            if input.dtype == "float32":
                datatype = "FP32"
            inputmtensor = MetadataTensor(
                name="input", datatype=datatype, shape=[input.shape[1]]
            )
            input_tensors.append(inputmtensor)

        output_tensors = []
        for output in model.outputs:
            datatype = None
            if output.dtype == "float32":
                datatype = "FP32"
            outputmtensor = MetadataTensor(
                name="output", datatype=datatype, shape=[output.shape[1]]
            )
            output_tensors.append(outputmtensor)

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
        try:
            load_model("model/" + model_name + ".keras")
            return ModelReadyResponse(name=model_name, ready=True)
        except ValueError:
            return ModelReadyResponse(name=model_name, ready=False)


class KserveCustomModel(AissembleOIPKServe):
    """
    Implements Custom predictor of AissembleOIPKServe for requesting model.
    """

    logger = LogManager.get_instance().get_logger("KserveCustomModel")

    def __init__(self, name: str, model_path: str, handler=None):
        super().__init__(name, handler)
        self.model = None
        self.name = name
        self.model_path = model_path
        self.handler = handler

    def load(self):
        self.model = load_model("model/" + self.model_path + ".keras")
        self.ready = True
        self.logger.info("Kserve Custom Model Loaded Successfully.")


if __name__ == "__main__":
    # DataplaneHandler is abstract base class, user should be extending this class for their implementation based on preferred API calls (REST or GRPC)
    model = KserveCustomModel(
        "convert_celsius_to_fahrenheit",
        "convert_celsius_to_fahrenheit",
        customFastAPIHandler,
    )
    model.load()
    ModelServer().start([model])
