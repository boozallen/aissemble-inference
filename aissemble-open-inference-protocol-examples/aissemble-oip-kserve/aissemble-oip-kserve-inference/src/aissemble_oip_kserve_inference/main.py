###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples KServe Inference
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import numpy as np
from typing import Optional

from tensorflow.keras.models import load_model

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
This example demonstrates how to use AissembleOIPKServe to create a Kserve model that is compatible with the 
aiSSEMBLE OIP handler. Define the handler the same as how it is for the other aiSSEMBLE OIP solutions, then pass it 
to the AissembleOIPKServe constructor along with the model name. In this example we then load the model and start the server
"""


class CustomFastAPIHandler(DataplaneHandler):
    def __init__(self):
        super().__init__()
        self.ready = False
        self.model = None

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
        input_tensors = []
        for input in self.model.inputs:
            datatype = None
            if input.dtype == "float32":
                datatype = Datatype.FP32
            inputmtensor = MetadataTensor(
                name="input", datatype=datatype, shape=[input.shape[1]]
            )
            input_tensors.append(inputmtensor)

        output_tensors = []
        for output in self.model.outputs:
            datatype = None
            if output.dtype == "float32":
                datatype = Datatype.FP32
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
        return ModelReadyResponse(name=model_name, ready=self.ready)

    def model_load(self, model_name) -> bool:
        self.model = load_model("model/" + model_name + ".keras")
        self.ready = True
        return True


if __name__ == "__main__":
    model_name = "convert_celsius_to_fahrenheit"
    oip_kserve = AissembleOIPKServe(name=model_name, handler=CustomFastAPIHandler())
    oip_kserve.load()
    oip_kserve.start()
