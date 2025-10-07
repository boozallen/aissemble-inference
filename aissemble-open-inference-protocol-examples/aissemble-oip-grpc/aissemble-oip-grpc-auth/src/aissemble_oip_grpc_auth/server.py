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
import asyncio
from aissemble_open_inference_protocol_grpc.aissemble_oip_grpc import AissembleOIPgRPC
from aissemble_oip_grpc_auth.auth_adapter import AuthAdapter
from aissemble_oip_grpc_auth.auth_handler import AuthHandler
import os


async def _main():
    grpc = AissembleOIPgRPC(model_handler=AuthHandler(), adapter=AuthAdapter())
    await grpc.start_server()


def run_server():
    print("Starting aiSSEMBLE OIP gRPC Auth Example...")
    print("Using AuthAdapter with role-based access control:")
    print("  - 'admin' role: Can access all endpoints")
    print("  - 'user' role: Can access only ServerReady")
    print("  - No role or unknown role: Denied access")
    print()

    # Set the Krausening configuration path so the properties will be picked up. This is assuming the script is being run
    # locally and would fail for dockerized deployments. This is only to ease running the example
    os.environ["KRAUSENING_BASE"] = os.getcwd() + "/src/resources/krausening/base/"

    asyncio.run(_main())
