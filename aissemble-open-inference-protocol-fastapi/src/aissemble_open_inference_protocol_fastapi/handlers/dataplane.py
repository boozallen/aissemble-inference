###
# #%L
# aiSSEMBLE::Open Inference Protocol::FastAPI
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from typing import Optional
from fastapi import status, HTTPException

from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelReadyResponse,
    ServerReadyResponse,
    ServerLiveResponse,
    ServerMetadataResponse,
)


class DataplaneHandler:
    @classmethod
    def infer(
        cls,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
        )

    @classmethod
    def model_metadata(
        cls,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
        )

    @classmethod
    def model_ready(
        cls,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelReadyResponse:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
        )

    @classmethod
    def server_ready(cls) -> ServerReadyResponse:
        return ServerReadyResponse(live=True)

    @classmethod
    def server_live(cls) -> ServerLiveResponse:
        return ServerLiveResponse(live=True)

    @classmethod
    def server_metadata(cls) -> ServerMetadataResponse:
        return ServerMetadataResponse(name="FastAPI", version="1.0", extensions=[])
