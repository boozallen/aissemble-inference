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
import asyncio
import os

from aissemble_open_inference_protocol_grpc.aissemble_oip_grpc import AissembleOIPgRPC
from aissemble_oip_grpc_inference.oip_handler import OIPHandler


async def _main():
    my_handler = OIPHandler()
    grpc = AissembleOIPgRPC(my_handler)
    grpc.model_load("Mathematics")
    await grpc.start_server()


def run_server():
    print("Starting aiSSEMBLE OIP gRPC Inference Example...")
    print("Available endpoints:")
    print("  - ModelInfer: Performs mathematical operations")
    print("  - ModelMetadata: Returns model metadata")
    print("  - ModelReady: Checks model readiness")
    print("  - ServerMetadata: Returns server metadata")
    print("  - ServerReady: Returns server readiness")
    print("  - ServerLive: Returns server liveness")
    print()
    print("Available models: multiply, add, square, default")
    print()

    os.environ["KRAUSENING_BASE"] = "src/resources/krausening/base"
    asyncio.run(_main())
