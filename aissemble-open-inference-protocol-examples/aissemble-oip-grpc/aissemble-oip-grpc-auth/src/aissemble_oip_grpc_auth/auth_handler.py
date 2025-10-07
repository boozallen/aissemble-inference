###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples::gRPC with Auth
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

from aissemble_open_inference_protocol_shared.handlers.model_handler import ModelHandler
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    MetadataTensor,
    Datatype,
)


class AuthHandler(ModelHandler):
    """
    Custom handler for auth example which implements simple functions for each endpoint.
    """

    def __init__(self):
        super().__init__()

    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        print(f"model_name={model_name}, model_version={model_version}")
        print(payload)
        return InferenceResponse(
            model_name=model_name, model_version=model_version, id="id", outputs=[]
        )

    def model_metadata(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        """
        Return metadata about the model.
        """
        input_tensors = [
            MetadataTensor(name="input", datatype=Datatype.FP32, shape=[1])
        ]

        output_tensors = [
            MetadataTensor(name="output", datatype=Datatype.FP32, shape=[1])
        ]

        return ModelMetadataResponse(
            name=model_name,
            versions=[model_version or "1.0"],
            platform="python",
            inputs=input_tensors,
            outputs=output_tensors,
        )

    def model_load(self, model_name) -> bool:
        return True
