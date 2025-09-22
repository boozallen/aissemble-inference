###
# #%L
# aiSSEMBLE::Open Inference Protocol::Shared
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from abc import ABC, abstractmethod
from typing import Optional

from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelReadyResponse,
)


class ModelHandler(ABC):
    @abstractmethod
    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        """
        Perform inference on the given inference request.

        Args:
            payload: The request to perform inference against.
            model_name: The model to perform inference against.
            model_version: The model version

        Returns:
            Results of the inference.
        """
        pass

    @abstractmethod
    def model_metadata(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        """
        Get metadata for a given model.

        Args:
            model_name: Name of the model.
            model_version: Version of the model.

        Returns:
            The metadata for the given model.
        """
        pass

    @abstractmethod
    def model_load(self, model_name: str) -> bool:
        """
        Loads the given model.

        Args:
            model_name: Name of the model to load.

        Returns:
            True if the model was successfully loaded, False otherwise.
        """
        pass

    def model_ready(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelReadyResponse:
        """
        Call to determine if the model is ready.

        Args:
            model_name: The model name.
            model_version: The model version.

        Returns:
            ModelReadyResponse for the given model.
        """
        return ModelReadyResponse(name=model_name, ready=True)


class DefaultModelHandler(ModelHandler):
    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        raise NotImplementedError

    def model_metadata(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        raise NotImplementedError

    def model_load(self, model_name: str) -> bool:
        raise NotImplementedError
