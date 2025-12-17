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
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #L%
###
from __future__ import annotations

from aissemble_oip.client.builder.raw_inference_buidler import RawInferenceBuilder
from aissemble_oip.client.oip_adapter import OipAdapter


class InferenceClient:
    """
    A facade of the entire client library. Supports one-line construction with zero configuration ceremony. It wraps
    controls invocation of OIP-compliant endpoints.

    ALL task-specific entry points (e.g., detect_object, summarize) are accessible from here.
    """

    def __init__(self, adapter: OipAdapter, endpoint: str):
        """
        Initializes the InferenceClient with the given adapter and endpoint.

        :param adapter: The OIP adapter to use for inference.
        :param endpoint: The endpoint URL for the inference service.
        """
        # TODO: Update to create these from configuration variables
        self.adapter = adapter
        self.endpoint = endpoint
    #
    # def object_detection(self, model_name: str) -> ObjectDetectionBuilder:
    #     """
    #     Creates a builder for object detection inference.
    #
    #     :param model_name: The name of the model to use.
    #     :return: An ObjectDetectionBuilder instance.
    #     """
    #     # TODO: Implement object detection builder creation
    #     pass
    #
    # def summarize(self, model_name: str) -> SummarizationBuilder:
    #     """
    #     Creates a builder for summarization inference.
    #
    #     :param model_name: The name of the model to use.
    #     :return: A SummarizationBuilder instance.
    #     """
    #     # TODO: Implement summarization builder creation
    #     pass

    def raw(self, model_name: str) -> RawInferenceBuilder:
        """
        Creates a builder for raw inference.

        :param model_name: The name of the model to use.
        :return: A RawInferenceBuilder instance.
        """
        # TODO: Implement raw inference builder creation
        pass
