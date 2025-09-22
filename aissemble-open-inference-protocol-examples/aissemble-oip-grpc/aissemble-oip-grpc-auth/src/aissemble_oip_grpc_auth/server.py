###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples::gRPC with Auth
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
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
