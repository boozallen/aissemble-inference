###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples::gRPC with Auth
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from typing import Optional
from aissemble_open_inference_protocol_shared.handlers.dataplane import DataplaneHandler
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelReadyResponse,
    MetadataTensor,
    Datatype,
    ServerReadyResponse,
)


class AuthHandler(DataplaneHandler):
    """
    Custom handler for auth example which implements simple functions for each endpoint.
    """

    def __init__(self):
        super().__init__()

    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        print(f"model_name={model_name}, model_version={model_version}")
        print(payload)
        return InferenceResponse(
            model_name=model_name, model_version=model_version, id="id", outputs=[]
        )

    def model_metadata(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        """
        Return metadata about the model.
        """
        input_tensors = [
            MetadataTensor(name="input", datatype=Datatype.FP32, shape=[1])
        ]

        output_tensors = [
            MetadataTensor(name="output", datatype=Datatype.FP32, shape=[1])
        ]

        return ModelMetadataResponse(
            name=model_name,
            versions=[model_version or "1.0"],
            platform="python",
            inputs=input_tensors,
            outputs=output_tensors,
        )

    def model_ready(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelReadyResponse:
        """
        Check if the model is ready for inference.
        """
        return ModelReadyResponse(name=model_name, ready=True)

    def server_ready(self) -> ServerReadyResponse:
        """
        Check if the server is ready."""
        return ServerReadyResponse(live=True)
