###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples::gRPC Inference
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import asyncio

from aissemble_open_inference_protocol_grpc.aissemble_oip_grpc import AissembleOIPgRPC
from aissemble_oip_grpc_inference.oip_handler import OIPHandler

my_handler = OIPHandler()
grpc = AissembleOIPgRPC(my_handler)


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

    asyncio.run(grpc.start())
