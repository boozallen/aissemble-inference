###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples::FastAPI Inference
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
import asyncio
from typing import Optional

import numpy as np
from krausening.logging import LogManager
from tensorflow.keras.models import load_model

from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import (
    AissembleOIPFastAPI,
)
from aissemble_open_inference_protocol_shared.handlers.model_handler import ModelHandler
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    MetadataTensor,
    ResponseOutput,
    Datatype,
)


class Handler(ModelHandler):
    """
    Implements Open Inferencing Protocol of FastAPI for requesting model inference.
    This example will load model called convert celsius to fahrenheit and kick off inferencing endpoint defined below.
    """

    logger = LogManager.get_instance().get_logger("Handler")

    def __init__(self):
        super().__init__()
        self.model = None

    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        # Model will take input data from the payload and make prediction to convert celsius to fahrenheit.
        output = self.model.predict(np.array(payload.inputs[0].data))
        # Need to convert to list so that we are align with output format.
        output_list = output.tolist()

        return InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            id=payload.id,
            outputs=[
                ResponseOutput(
                    name=model_name,
                    shape=payload.inputs[0].shape,
                    datatype=Datatype.FP32,
                    data=output_list,
                )
            ],
        )

    def model_metadata(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        input_tensors = []
        for input in self.model.inputs:
            datatype = None
            if input.dtype == "float32":
                datatype = Datatype.FP32
            inputmtensor = MetadataTensor(
                name="input", datatype=datatype, shape=[input.shape[1]]
            )
            input_tensors.append(inputmtensor)

        output_tensors = []
        for output in self.model.outputs:
            datatype = None
            if output.dtype == "float32":
                datatype = Datatype.FP32
            outputmtensor = MetadataTensor(
                name="output", datatype=datatype, shape=[output.shape[1]]
            )
            output_tensors.append(outputmtensor)

        return ModelMetadataResponse(
            name=model_name,
            versions=[model_version] if model_version else None,
            platform="python",
            inputs=input_tensors,
            outputs=output_tensors,
        )

    def model_load(self, model_name) -> bool:
        self.model = load_model("model/" + model_name + ".keras")
        self.logger.info("Model loaded successfully")
        return True


async def start():
    fastapi = AissembleOIPFastAPI(Handler())
    fastapi.model_load("convert_celsius_to_fahrenheit")
    await fastapi.start_server()


def main():
    asyncio.run(start())
