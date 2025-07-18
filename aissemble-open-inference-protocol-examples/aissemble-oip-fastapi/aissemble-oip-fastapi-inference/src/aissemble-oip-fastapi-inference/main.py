###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples::FastAPI Inference
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import numpy as np
from typing import Optional
from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import (
    AissembleOIPFastAPI,
)
from tensorflow.keras.models import load_model
from aissemble_open_inference_protocol_shared.handlers.dataplane import (
    DataplaneHandler,
)
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelReadyResponse,
    MetadataTensor,
    ResponseOutput,
    Datatype,
)


class Handler(DataplaneHandler):
    """
    Implements Open Inferencing Protocol of FastAPI for requesting model.
    This example will load model called convert celsius to fahrenheit and kick off inferencing endpoint defined below.
    If this handlers doesn't implement one of Open Inferencing Protocol endpoints it would default to DataplaneHandler
    """

    def __init__(self):
        super().__init__()

    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        model = load_model("model/" + model_name + ".keras")
        # Model will take input data from the payload and make prediction to convert celsius to fahrenheit.
        output = model.predict(np.array(payload.inputs[0].data))
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
                    data=[output_list],
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


app = AissembleOIPFastAPI(Handler).app
