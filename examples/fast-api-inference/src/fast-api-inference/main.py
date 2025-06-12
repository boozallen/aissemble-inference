###
# #%L
# aiSSEMBLE::Open Inference Protocol FastAPI Examples
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

from aissemble_open_inference_protocol_fastapi.handlers.dataplane import (
    DataplaneHandler,
)
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelReadyResponse,
    MetadataTensor,
    ServerLiveResponse,
    ServerMetadataResponse,
    ServerReadyResponse,
    ResponseOutput,
    Datatype,
)


class Handler(DataplaneHandler):
    """
    Implements Open Inferencing Protocol of FastAPI for requesting model.
    This example will load model called convert celsius to fahrenheit and kick off inferencing endpoint defined below.
    If this handlers doesn't implement one of Open Inferencing Protocol endpoints it would default to DefaultHandler
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
        # Return a stub ModelMetadataResponse
        return ModelMetadataResponse(
            name=model_name,
            versions=[model_version] if model_version else None,
            platform="python",
            inputs=[MetadataTensor(name="input", datatype="FP32", shape=[1])],
            outputs=[MetadataTensor(name="output", datatype="FP32", shape=[1])],
        )

    def model_ready(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelReadyResponse:
        # Testing: always ready
        return ModelReadyResponse(name=model_name, ready=True)

    def server_ready(
        self,
    ) -> ServerReadyResponse:
        # Testing: always ready
        return ServerReadyResponse(live=True)

    def server_live(
        self,
    ) -> ServerLiveResponse:
        # Testing: always live
        return ServerLiveResponse(live=True)

    def server_metadata(
        self,
    ) -> ServerMetadataResponse:
        # Return a stub ServerMetadataResponse
        return ServerMetadataResponse(
            name="Server",
            version="v2",
            extensions=["extension"],
        )


app = AissembleOIPFastAPI(Handler).app
