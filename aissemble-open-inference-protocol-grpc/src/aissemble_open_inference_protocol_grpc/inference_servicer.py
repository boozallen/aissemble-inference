###
# #%L
# aiSSEMBLE::Open Inference Protocol::gRPC
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import grpc

from aissemble_open_inference_protocol_grpc.grpcInferenceService_pb2_grpc import (
    GRPCInferenceServiceServicer,
)


# TODO One big question here is do we want to use the same handler across our solutions? It makes implementation easy
#  and easy to migration or add solutions. We could store the handler in an aissemble-oip-shared module so they arent
#  reliant on each other. A counterpoint is a project only implementing grpc looking at the oip docs would find it odd
#  that their handler is taking in different formatted data
class InferenceServicer(GRPCInferenceServiceServicer):
    def __init__(self, handler):
        self.handler = handler
