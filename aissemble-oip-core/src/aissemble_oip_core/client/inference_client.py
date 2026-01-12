###
# #%L
# aiSSEMBLE::Open Inference Protocol::Core
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #L%
###
from __future__ import annotations

from aissemble_oip_core.client.builder.object_detection_builder import (
    ObjectDetectionBuilder,
)
from aissemble_oip_core.client.builder.raw_inference_builder import RawInferenceBuilder
from aissemble_oip_core.client.oip_adapter import OipAdapter


class InferenceClient:
    """A facade of the entire client library. Supports one-line construction with zero configuration ceremony. It wraps
    controls invocation of OIP-compliant endpoints.

    ALL task-specific entry points (e.g., detect_object, summarize) are accessible from here.
    """

    def __init__(self, adapter: OipAdapter, endpoint: str):
        """Initializes the InferenceClient with the given adapter and endpoint.

        Args:
            adapter: The OIP adapter to use for inference.
            endpoint: The endpoint URL for the inference service.
        """
        # TODO: Update to create these from configuration variables
        self.adapter = adapter
        self.endpoint = endpoint

    def raw(self, model_name: str) -> RawInferenceBuilder:
        """Creates a builder for raw inference.

        Args:
            model_name: The name of the model to use.

        Returns:
            A RawInferenceBuilder instance.
        """
        # TODO: Implement raw inference builder creation
        pass

    def detect_object(self, model_name: str | None = None) -> ObjectDetectionBuilder:
        """Creates a builder for object detection inference.

        Args:
            model_name: Optional name of the model to use

        Returns:
            An ObjectDetectionBuilder instance configured for this client

        Example:
            result = client.detect_object("yolov8").image("photo.jpg").confidence(0.6).run()
        """
        builder = ObjectDetectionBuilder()
        builder = builder.with_adapter(self.adapter)
        if model_name:
            builder = builder.with_model(model_name)
        return builder
