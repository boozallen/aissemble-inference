###
# #%L
# aiSSEMBLE::Open Inference Protocol KServe Examples
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
import os

from kserve import InferRequest, InferInput
from kserve.inference_client import InferenceGRPCClient


async def main():
    client = InferenceGRPCClient(
        url=os.environ.get("INGRESS_HOST", "localhost")
        + ":"
        + os.environ.get("INGRESS_PORT", "8081"),
        channel_args=[
            ("grpc.ssl_target_name_override", os.environ.get("SERVICE_HOSTNAME", ""))
        ],
    )

    infer_input = InferInput(
        name="sample", shape=[3, 1], datatype="FP32", data=[5.0, 59.0, 80.0]
    )
    request = InferRequest(
        infer_inputs=[infer_input],
        model_name="convert_celsius_to_fahrenheit",
        model_version="1.0",
        request_id="1",
        from_grpc=True,
    )
    res = await client.infer(infer_request=request)
    print(res)


asyncio.run(main())
