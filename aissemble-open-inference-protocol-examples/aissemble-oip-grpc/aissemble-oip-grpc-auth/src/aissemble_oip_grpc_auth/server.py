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


def run_server():
    print("Starting aiSSEMBLE OIP gRPC Auth Example...")
    print("Using AuthAdapter with role-based access control:")
    print("  - 'admin' role: Can access all endpoints")
    print("  - 'user' role: Can access only ServerReady")
    print("  - No role or unknown role: Denied access")
    print()

    os.environ["KRAUSENING_BASE"] = "src/resources/krausening/base"
    grpc_server = AissembleOIPgRPC(
        handler=AuthHandler(),
        adapter=AuthAdapter(),
        grpc_properties="oip.properties",
    )
    asyncio.run(grpc_server.start())
