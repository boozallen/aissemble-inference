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
from abc import ABC, abstractmethod

from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelReadyResponse,
    ServerReadyResponse,
    ServerLiveResponse,
    ServerMetadataResponse,
)


class DataplaneHandler(ABC):
    @abstractmethod
    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        pass

    @abstractmethod
    def model_metadata(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        pass

    @abstractmethod
    def model_ready(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelReadyResponse:
        pass

    def server_ready(self) -> ServerReadyResponse:
        return ServerReadyResponse(live=True)

    def server_live(self) -> ServerLiveResponse:
        return ServerLiveResponse(live=True)

    def server_metadata(self) -> ServerMetadataResponse:
        return ServerMetadataResponse(name="FastAPI", version="1.0", extensions=[])
