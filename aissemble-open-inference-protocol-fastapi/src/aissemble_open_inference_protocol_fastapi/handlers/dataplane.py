###
# #%L
# aiSSEMBLE::Open Inference Protocol::FastAPI
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from abc import ABC, abstractmethod
from typing import Optional

from aissemble_open_inference_protocol_fastapi.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
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
