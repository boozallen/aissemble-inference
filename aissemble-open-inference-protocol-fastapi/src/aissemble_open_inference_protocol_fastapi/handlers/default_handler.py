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

from aissemble_open_inference_protocol_fastapi.handlers.dataplane import (
    DataplaneHandler,
)
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelReadyResponse,
)


class DefaultHandler(DataplaneHandler):
    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
        )

    def model_metadata(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
        )

    def model_ready(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelReadyResponse:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
        )
