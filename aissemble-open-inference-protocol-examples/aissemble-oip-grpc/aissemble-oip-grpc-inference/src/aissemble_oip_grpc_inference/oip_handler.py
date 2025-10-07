###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples::gRPC Inference
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
from typing import Optional

from krausening.logging import LogManager

from aissemble_open_inference_protocol_shared.handlers.model_handler import ModelHandler
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelReadyResponse,
    MetadataTensor,
    ResponseOutput,
    Datatype,
    TensorData,
)


class OIPHandler(ModelHandler):
    """
    Custom handler that implements all Open Inference Protocol endpoints.
    This example demonstrates how to implement custom handlers for each endpoint:
    - ModelInfer: Performs simple mathematical operations on input data
    - ModelMetadata: Returns metadata about the model
    - ModelReady: Checks if the model is ready for inference
    - ServerMetadata: Returns server information
    - ServerReady: Returns server readiness status
    - ServerLive: Returns server liveness status
    """

    logger = LogManager.get_instance().get_logger("OIPHandler")

    def __init__(self):
        super().__init__()

    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        """
        Perform inference using the provided input data.
        This example performs simple mathematical operations based on the model name.
        """
        self.logger.info(
            f"Received inference request for model: {model_name}, version: {model_version}"
        )

        if not payload.inputs:
            raise ValueError("No input data provided")

        input_tensor = payload.inputs[0]

        # Get the data from the TensorData object
        try:
            data_list = [int(x) for x in input_tensor.data.root]
            self.logger.info(f"Processing input data: {data_list}")
        except Exception as e:
            self.logger.error(f"Error processing data: {e}")
            raise ValueError(f"Invalid input data format: {e}")

        if model_name == "multiply":
            result = [x * 2 for x in data_list]
        elif model_name == "add":
            result = [x + 10 for x in data_list]
        elif model_name == "square":
            result = [x**2 for x in data_list]
        else:
            result = data_list

        self.logger.info(f"Output data: {result}")
        # Create response with proper TensorData structure
        response = InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            id=payload.id,
            outputs=[
                ResponseOutput(
                    name="output-0",
                    shape=input_tensor.shape,
                    datatype=input_tensor.datatype,
                    data=TensorData(root=result),
                    parameters=payload.outputs[0].parameters,
                )
            ],
            parameters=payload.parameters,
        )
        return response

    def model_metadata(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        """
        Return metadata about the model including input/output tensor specifications.
        """
        self.logger.info(
            f"Received model metadata request for model: {model_name}, version: {model_version}"
        )

        return ModelMetadataResponse(
            name=model_name,
            versions=[model_version] if model_version else None,
            platform="python",
            inputs=[MetadataTensor(name="input", datatype=Datatype.INT64, shape=[1])],
            outputs=[MetadataTensor(name="output", datatype=Datatype.INT64, shape=[1])],
        )

    def model_ready(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelReadyResponse:
        """
        Check if the model is ready for inference.
        This example considers specific models as ready.
        """
        self.logger.info(
            f"Received model ready request for model: {model_name}, version: {model_version}"
        )

        ready_models = ["multiply", "add", "square", "default"]
        is_ready = model_name in ready_models

        return ModelReadyResponse(name=model_name, ready=is_ready)

    def model_load(self, model_name) -> bool:
        self.logger.info("Model has been loaded.")
        return True
