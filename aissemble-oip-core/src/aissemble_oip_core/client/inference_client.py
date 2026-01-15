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

from typing import Dict, List

from aissemble_oip_core.client.builder.object_detection_builder import (
    ObjectDetectionBuilder,
)
from aissemble_oip_core.client.builder.raw_inference_builder import RawInferenceBuilder
from aissemble_oip_core.client.builder.summarization_builder import (
    SummarizationBuilder,
)
from aissemble_oip_core.client.oip_adapter import OipAdapter
from aissemble_oip_core.client.registry import ModuleRegistry


class InferenceClient:
    """A facade of the entire client library. Supports one-line construction with zero configuration ceremony. It wraps
    controls invocation of OIP-compliant endpoints.

    ALL task-specific entry points (e.g., detect_object, summarize) are accessible from here.

    The client supports dynamic module discovery via Python entry points. Installed
    OIP modules (e.g., aissemble-oip-yolo) automatically register their builders,
    translators, and runtimes.

    Example:
        from aissemble_oip_core.client import InferenceClient

        client = InferenceClient(adapter, endpoint)

        # List available modules
        print(client.list_available_modules())

        # Use object detection (uses discovered or built-in builder)
        result = client.detect_object("yolov8").image("photo.jpg").run()
    """

    def __init__(self, adapter: OipAdapter, endpoint: str):
        """Initializes the InferenceClient with the given adapter and endpoint.

        Args:
            adapter: The OIP adapter to use for inference.
            endpoint: The endpoint URL for the inference service.
        """
        self.adapter = adapter
        self.endpoint = endpoint
        self._registry = ModuleRegistry.instance()

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

        If a model-specific builder is registered (e.g., from aissemble-oip-yolo),
        it will be used. Otherwise, falls back to the default ObjectDetectionBuilder.

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

    def summarize(self, model_name: str | None = None) -> SummarizationBuilder:
        """Creates a builder for text summarization inference.

        Args:
            model_name: Optional name of the summarization model to use

        Returns:
            A SummarizationBuilder instance configured for this client

        Example:
            result = client.summarize("bart-large") \
                .text("Long article text here...") \
                .max_length(100) \
                .run()
            print(result.summary)
        """
        builder = SummarizationBuilder()
        builder = builder.with_adapter(self.adapter)
        if model_name:
            builder = builder.with_model(model_name)
        return builder

    def list_available_modules(self) -> Dict[str, List[str]]:
        """List all discovered OIP modules.

        Returns:
            Dictionary mapping category to list of available module names.
            Categories: runtimes, translators, builders

        Example:
            modules = client.list_available_modules()
            # {'runtimes': ['yolo'], 'translators': ['yolo', 'object_detection'], ...}
        """
        return self._registry.list_available()

    def get_translator(self, name: str):
        """Get a translator class by name from the registry.

        Args:
            name: The registered name of the translator

        Returns:
            The translator class, or None if not found
        """
        return self._registry.get_translator(name)

    def get_runtime(self, name: str):
        """Get a runtime class by name from the registry.

        Args:
            name: The registered name of the runtime

        Returns:
            The runtime class, or None if not found
        """
        return self._registry.get_runtime(name)
