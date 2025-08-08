###
# #%L
# aiSSEMBLE::Open Inference Protocol KServe Examples
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
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
